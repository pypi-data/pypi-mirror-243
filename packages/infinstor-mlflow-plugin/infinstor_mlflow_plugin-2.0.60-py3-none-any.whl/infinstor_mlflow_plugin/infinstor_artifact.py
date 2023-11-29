import pathlib
import posixpath
from typing import List, Tuple, Union
from infinstor_mlflow_plugin.tokenfile import get_token, get_id_token
from .utils import set_builtins_with_serverside_config
from infinstor_mlflow_plugin import login
from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository
import os
import builtins
import urllib
from urllib.parse import quote, quote_plus
from urllib.request import unquote, urlretrieve
from requests.exceptions import HTTPError
import requests
import mlflow
from mlflow.utils.file_utils import relative_path_to_artifact_path
from mlflow.entities import FileInfo
import xml.etree.ElementTree as ET
import xml.etree.ElementTree 
from mlflow.exceptions import MlflowException
from . import tokenfile
import dataclasses
import jsons
import concurrent.futures

import logging
from .utils import _get_logger
logger:logging.Logger = _get_logger(__name__)

def our_parse_s3_uri(uri):
    """Parse an S3 URI, returning (bucket, path)"""
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme != "s3":
        raise Exception("Not an S3 URI: %s" % uri)
    path = parsed.path
    if path.startswith("/"):
        path = path[1:]
    return parsed.netloc, path

def _log_requests_Response(resp:requests.Response):
    logger.info(f"response.request.method={resp.request.method} response.request.url={resp.request.url}")
    logger.info(f"response.request.headers={resp.request.headers}")
    # response.request.body can be _io.BufferedReader.  This will result in the error: TypeError: object of type '_io.BufferedReader' has no len()
    if resp.request.body:
        if isinstance(resp.request.body, (str,bytes)): 
            logger.info(f"response.request.body (truncated < 1024)={resp.request.body if len(resp.request.body) < 1024 else resp.request.body[:1024]}")
        else:
            logger.info(f"response.request.body type={type(resp.request.body)}")
    logger.info(f"response.status_code={resp.status_code}")
    logger.info(f"response.headers={resp.headers}")
    if resp.content: 
        if isinstance(resp.content, str) or isinstance(resp.content, bytes): 
            logger.info(f"response.content (truncated < 1024)={resp.content if len(resp.content) < 1024 else resp.content[:1024]}")
        else:
            logger.info(f"response.content type={type(resp.content)}")

@dataclasses.dataclass
class CreateMultiPartUploadPresignedUrlInfo:        
    chunk_num:int
    """chunk number for this multipart upload"""
    ps_url:str
    """presigned url for above chunk number"""
    
@dataclasses.dataclass
class CreateMultiPartUploadResp:
    upload_id: str 
    ps_url_infos_for_mult_part:List[CreateMultiPartUploadPresignedUrlInfo] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class CompleteMultiPartUploadComplatedPartInfo:
    PartNumber:int
    ETag:str

@dataclasses.dataclass
class CompleteMultiPartUploadReq:
    upload_id:str
    Parts:List[CompleteMultiPartUploadComplatedPartInfo] = dataclasses.field(default_factory=list)
        
class InfinStorArtifactRepository(S3ArtifactRepository):
    """LocalArtifactRepository provided through plugin system"""
    is_plugin = True

    def __init__(self, artifact_uri:str):
        """
        _summary_

        Args:
            artifact_uri (str): This will not always be the run's artifact root URI (s3://<bucket_name>/path/to/run_id).  It can also be some path under the run's artifact root URI: similar to s3://<bucket_name>/path/to/run_id/path/to/subdir.  here run's artifact root URI is s3://<bucket_name>/path/to/run_id. For an example of the latter, see mlflow.git/tests/models/test_model.py(243)test_model_load_input_example_numpy().  Also the recipe.train() step of mlflow-recipe-examples/regression

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        #######
        # for log_artifact() or log_artifacts() call, we do not need to check if logging is happening under a 'deleted experiments', since log_artifact() and log_artifacts() need an active run and creating this run will fail under a deleted experiment
        #######
        self.srvc = login.bootstrap_from_mlflow_rest() 
        set_builtins_with_serverside_config(self.srvc)
        id_token, service = get_id_token(self.srvc['region'])
        rj = login.get_customer_info_rest(id_token)
        if 'usePresignedUrlForMLflow' in rj and rj['usePresignedUrlForMLflow'] == 'true':
            logger.info('InfinStorArtifactRepository: usePresignedUrlForMLflow='
                    + str(rj['usePresignedUrlForMLflow']))
            self.use_presigned_url_for_mlflow = True
        else:
            self.use_presigned_url_for_mlflow = False
        
        # default artifact location: infinstor-mlflow-artifacts/mlflow-artifacts/<user_name>/1/1-16705263394030000000004/sklearn-model/MLmodel
        # if create_experiment() specifies an artifact uri:  <experiment_artifiact_uri>/<run-id>/...
        #
        # Ugly, but we need to determine the run_id from the artifact URI.
        last_slash = artifact_uri.rfind('/')
        if last_slash == -1:
            raise ValueError('artifact_uri ' + str(artifact_uri) + ' does not include run_id')

        # Note that self.subpath_after_runid is relative to the run's artifact root URI.  
        success, self.this_run_id, self.path_upto_including_runid, self.subpath_after_runid = self.parse_run_id_from_uri(artifact_uri)
        if not success:
            raise ValueError('Unable to extract run_id from artifact_uri ' + str(artifact_uri))
        if self.use_presigned_url_for_mlflow:
            logger.info('InfinStorArtifactRepository.initialized. artifact_uri=' + artifact_uri
                + ', run_id=' + self.this_run_id
                + ', path_upto_including_runid=' + str(self.path_upto_including_runid)
                + ', subpath_after_runid=' + str(self.subpath_after_runid))
        super().__init__(artifact_uri)

    def is_run_id_valid(self, run_id):
        ind = run_id.find('-')
        if ind == -1:
            return False
        try:
            exp_id = int(run_id[:ind])
            run_id_portion = int(run_id[ind+1:])
            return True
        except ValueError as verr:
            return False

    def parse_run_id_from_uri(self, artifact_uri:str) -> Tuple[bool, str, str]:
        """

        Args:
            artifact_uri (_type_): the expected format is similar to s3://<bucket>/path/to/run_id/sub_path/after/run_id
            
            Example URIs:        
                default URI: similar to s3://<bucket>/infinstor-mlflow-artifacts/mlflow-artifacts/<user_name>/1/1-16705263394030000000004/sklearn-model/MLmodel                
                if create_experiment() specifies an artifact uri:  <experiment_artifiact_uri>/<run-id>/...

        Returns:
            Tuple[bool, str, str, str]: returns the tuple success, run_id, path_upto_including_runid, subpath_after_run_id.  The subpath_after_run_id and path_upto_including_runid has no leading or trailing '/'
        """
        au_parts:list[str] = artifact_uri.lstrip('/').rstrip('/').split('/')
        # traverse each path element of the artifact_uri from right to left
        for ind in range(len(au_parts), 0, -1):
            run_id = au_parts[ind-1]
            
            # if element at 'ind-1' is a run_id
            if self.is_run_id_valid(run_id):
                subpath_after_runid = ''
                # get subpath_after_runid: traverse all elements of the artifact_uri after the run_id: from ind to len(au_parts). 'ind-1' is the run_id.
                for ind1 in range(ind, len(au_parts), 1):
                    subpath_after_runid = subpath_after_runid + '/' + au_parts[ind1]
                subpath_after_runid = subpath_after_runid.lstrip('/').rstrip('/')
                
                # get path_upto_runid.  'ind-1' is the index for run_id.  for an s3 url like s3://<bucket>/path/to/run_id/sub_path/after/run_id, the index[3:ind] returns [path, to, run_id]
                path_upto_including_runid:str = '/'.join(au_parts[3:ind])
                path_upto_including_runid.lstrip('/').rstrip('/')
                return True, run_id, path_upto_including_runid, subpath_after_runid
        return False, '', '', ''

    def _get_s3_client(self):
        if not self.use_presigned_url_for_mlflow:
            return super()._get_s3_client()
        return None
    
    @classmethod
    def pretty_print_prep_req(cls, req:requests.PreparedRequest):
        return '{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        )
    
    def _process_parallel_batch(self, parallel_batch, parallel_batch_size, chunk_max_size, num_of_chunks, st_size, comp_multi_part_upload_arg, create_mult_upload_resp, fp):
        print(f"_process_parallel_batch: Entered. parallel_batch={parallel_batch}, parallel_batch_size={parallel_batch_size}, chunk_max_size={chunk_max_size}, num_of_chunks={num_of_chunks}, st_size={st_size}", flush=True)
        executor:concurrent.futures.ThreadPoolExecutor; requests_futures:List[concurrent.futures.Future] = []
        start_chunk = parallel_batch * parallel_batch_size
        end_chunk = min(start_chunk + parallel_batch_size, num_of_chunks)
        print(f"_process_parallel_batch: start_chunk={start_chunk}, end_chunk={end_chunk}", flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_batch_size) as executor:
            for zero_base_chunk_num in range(start_chunk, end_chunk):
                chunk_num = zero_base_chunk_num + 1
                create_mult_upload_ps_info:CreateMultiPartUploadPresignedUrlInfo = create_mult_upload_resp.ps_url_infos_for_mult_part[chunk_num-1]
                # for last chunk, send all data; for earlier chunks, send chunkSize
                this_chunk_size:int =  (st_size - ((num_of_chunks-1)*chunk_max_size) ) if (chunk_num == num_of_chunks) else chunk_max_size
                logger.info(f"uploading chunk_num={chunk_num} this_chunk_size={this_chunk_size}; st_size={st_size}")

                # data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
                # use the presigned URL
                # resp.headers={'x-amz-id-2': 'rN8vRBufk/Pcn64yzN8iclJ4gvT4soMRJso0qb9exlUk+cpGMzkxa+c7MrmiPH7MKn10Aywzo8E=', 'x-amz-request-id': '5VQZB40H83CYTQ15', 'Date': 'Tue, 13 Jun 2023 06:13:47 GMT', 'ETag': '"ae12b6d1eb2400a7fdd608092e4deff2"', 'x-amz-server-side-encryption': 'AES256', 'Server': 'AmazonS3', 'Content-Length': '0'}
                logger.debug(f"\n##############\nStarting requests.put() for chunk_num={chunk_num}\n########################")
                # reqs_resp:requests.Response = requests.put(create_mult_upload_ps_info.ps_url, data=fp.read(this_chunk_size))
                data=fp.read(this_chunk_size)
                requests_future:concurrent.futures.Future = executor.submit(requests.put, create_mult_upload_ps_info.ps_url, data=data)
                requests_futures.append(requests_future)

            for ind in range(len(requests_futures)):
                chunk_num = start_chunk + ind + 1
                requests_future:concurrent.futures.Future = requests_futures[ind]
                reqs_resp:requests.Response = None
                try:
                    # timeout: The number of seconds to wait for the result if the future
                    # Returns:
                    #     The result of the call that the future represents.
                    # Raises:
                    #     CancelledError: If the future was cancelled.
                    #     TimeoutError: If the future didn't finish executing before the given timeout.
                    #     Exception: If the call raised then that exception will be raised.
                    reqs_resp:requests.Response = requests_future.result()
                    logger.info(f"upload chunk_num={chunk_num}: completed. reqs_resp={reqs_resp}")
                    if logger.getEffectiveLevel() == logging.DEBUG: logger.debug(f"upload chunk_num={chunk_num}: requests_future.result() = reqs_resp = {reqs_resp}")
                except Exception as e:
                    logger.error(f"caught exception when uploading chunk_num={chunk_num}: e", exc_info=e)
                    raise Exception(f"Error: multipart upload chunk {chunk_num} returned error {e}. Failing entire upload")
                # if 'reqs_resp' is set, then no exception was thrown above.
                if reqs_resp.status_code == 200:
                    # see CompletedPartTypeDef which defines the type for 'CompletedPart'
                    comp_multi_part_upload_arg.Parts.append( CompleteMultiPartUploadComplatedPartInfo(chunk_num, reqs_resp.headers["ETag"]) )
                elif reqs_resp.status_code == 403:
                    _log_requests_Response(reqs_resp)
                    raise Exception(f"Error: multipart upload chunk {chunk_num} returned error 403. Failing entire upload")
                else:
                    _log_requests_Response(reqs_resp)
                    raise Exception(f"Error: multipart upload chunk {chunk_num} returned code {reqs_resp.status_code}. Failing entire upload")

    def _upload_file(self, s3_client, local_file:Union[str,pathlib.Path], bucket:str, key:str):
        """
        _summary_

        Args:
            s3_client (_type_): _description_
            local_file (Union[str,pathlib.Path]): local_file can be pathlib.Path: see tests/artifacts/test_artifacts.py::test_download_artifacts_with_dst_path()
            upload_bucket (str): _description_
            upload_key (str): this is derived from artifact_uri and is under artifact_uri.  See S3ArtifactRepository._upload_file() implementation

        Raises:
            MlflowException: _description_

        Returns:
            _type_: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._upload_file(s3_client, local_file, bucket, key)
        logger.info('InfinStorArtifactRepository._upload_file: local_file=' + str(local_file)\
                + ', bucket=' + str(bucket) + ', key=' + key)
        (au_bucket, au_artifact_path) = our_parse_s3_uri(self.artifact_uri)
        self._verify_listed_object_contains_artifact_path_prefix(
            listed_object_path=key, artifact_path=au_artifact_path
        )
        if au_bucket != bucket:
            raise MlflowException(
                "InfinStorArtifactRepository:_upload_file bucket mismatch. artifact_bucket="\
                        + au_bucket + ", bucket in=" + bucket)
        
        # at this point we've verified that 
        # -- au_artifact_path has a run_id (stored in self.this_run_id and done by __init__() )
        # -- 'upload_key' is under 'au_artifact_path' 
        # -- and the au_bucket and upload_bucket are the same.
        # with this, we have verified that 'upload_bucket' and 'upload_key' represent a location under the run's artifact root URI.
        # 
        # Now get a new_key that is compliant with get_presigned_url() API
        success:bool; run_id:str; subpath_after_run_id:str
        success, run_id, _, subpath_after_run_id = self.parse_run_id_from_uri(f's3://{bucket}/{key}')
        upload_file_using_put_object = False if os.getenv("INFINSTOR_ENABLE_MULTIPART_UPLOAD") else True
        if upload_file_using_put_object:
            ps_url = self.get_presigned_url(subpath_after_run_id, 'put_object')
            # open() accpets os.PathLike protocol: see https://docs.python.org/3/library/functions.html#open
            with open(local_file, 'rb') as fp:
                # do not use requests.put(...,data=fp.read(),...): if file > 2 GB, ssl.py will throw "E   OverflowError: string longer than 2147483647 bytes"
                # file_data = fp.read()
                # 
                # but for zero byte files, do not use fp.read() since requests.put() adds the header "transfer-encoding: chunked".  When a presigned url is used, it results in the error below:
                # <Error><Code>NotImplemented</Code><Message>A header you provided implies functionality that is not implemented</Message><Header>Transfer-Encoding</Header>
                stat_res:os.stat_result = os.stat(local_file)
                if stat_res.st_size == 0:
                    hr:requests.Response = requests.put(ps_url, data=fp.read(), timeout=7200)
                else:
                    hr:requests.Response = requests.put(ps_url, data=fp, timeout=7200)
                if (hr.status_code != 200):
                    logger.error(f'InfinStorArtifactRepository._upload_file: WARNING. upload resp != 200. response.status_code={hr.status_code};\n  response.content={hr.content};\n  response.headers={hr.headers};\n  response.request={InfinStorArtifactRepository.pretty_print_prep_req(hr.request)}')
        else:
            create_mult_upload_resp:CreateMultiPartUploadResp = None
            try:
                with open(local_file, "rb") as fp:
                    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
                    # 
                    # The following table provides multipart upload core specifications. For more information, see Uploading and copying objects using multipart upload.
                    # Item	Specification
                    # Maximum object size	5 TiB
                    # Maximum number of parts per upload	10,000
                    # Part numbers	1 to 10,000 (inclusive)
                    # Part size	5 MiB to 5 GiB. There is no minimum size limit on the last part of your multipart upload.
                    # Maximum number of parts returned for a list parts request	1000
                    # Maximum number of multipart uploads returned in a list multipart uploads request	1000
                    # 
                    # From above: min 'part size' = 5 MiB (except 'last part', which has no minimum); max 'part size' = 5GiB; max number of parts = 10,000; max size of object = 5 TiB
                    # Given above: if file_size < 100 MiB, upload as a 'single part'; if file_size > 100 MiB, upload as multple parts
                    stat_res:os.stat_result = os.stat(local_file)
                    chunk_max_size:int = 100*1000*1000  # 100 MiB
                    # using '+ 1' since the computed RHS is relative to zero and not 1.
                    num_of_chunks:int = int(stat_res.st_size / chunk_max_size) + 1
                    logger.info(f"Initializing: file_size={stat_res.st_size}; chunk_max_size={chunk_max_size}; num_of_chunks={num_of_chunks}")
                    
                    # create presigned URL for each chunk
                    create_mult_upload_resp = self.get_presigned_url(subpath_after_run_id, 'create_multipart_upload', num_of_chunks=num_of_chunks)
                    upload_id = create_mult_upload_resp.upload_id

                    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/complete_multipart_upload.html#
                    comp_multi_part_upload_arg:CompleteMultiPartUploadReq = CompleteMultiPartUploadReq(upload_id)

                    parallel_batch_size = 8
                    num_parallel_batches = int(num_of_chunks/parallel_batch_size)
                    if (num_of_chunks % parallel_batch_size) > 0:
                        num_parallel_batches += 1
                    for parallel_batch in range(0, num_parallel_batches):
                        self._process_parallel_batch(parallel_batch, parallel_batch_size, chunk_max_size, num_of_chunks, stat_res.st_size, comp_multi_part_upload_arg, create_mult_upload_resp, fp)
                        create_mult_upload_resp = self.get_presigned_url(subpath_after_run_id, 'refresh_multipart_upload', num_of_chunks=num_of_chunks, upload_id=upload_id)

                    # complete the multipart upload
                    self.get_presigned_url(subpath_after_run_id, 'complete_multipart_upload', comp_multi_upload=comp_multi_part_upload_arg)
            except Exception as e:
                logger.error(f"Exception caught={e}", exc_info=e)
                # if createMultipartUpload() was called earlier and succeeded, then abort it
                if create_mult_upload_resp:
                    logger.info("\n##############\nStarting s3_client.abort_multipart_upload()\n########################")
                    resp:str = self.get_presigned_url(subpath_after_run_id, 'abort_multipart_upload', upload_id=upload_id)
                    logger.info(f"self.get_presigned_url(method=abort_multipart_upload..)={resp}")
                # re raise the exception so that the caller can handle the error
                raise

    def _download_file(self, remote_file_path:str, local_path:Union[str,pathlib.Path]):
        """
        _summary_

        Args:
            remote_file_path (str): 'remote_file_path' is relative to 'artifact_uri'.  is is a path under under artifact_uri.  See S3ArtifactRepository._download_file() for details
            local_path (Union[str,pathlib.Path]): local_file can be pathlib.Path: see tests/artifacts/test_artifacts.py::test_download_artifacts_with_dst_path()

        Returns:
            _type_: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._download_file(remote_file_path, local_path)
        # Note: subpath_after_runid is relative to the run's artifact root URI (see __init__()).  so remote_file_path is also relative to the run's artifact root URI, is under the run's artifact root URI, which is what we want.
        remote_file_path = self.subpath_after_runid + '/' + remote_file_path if self.subpath_after_runid else remote_file_path
        logger.info('InfinStorArtifactRepository._download_file: remote_file_path=' + str(remote_file_path) + ', local_path=' + str(local_path))
        ps_url = self.get_presigned_url(remote_file_path, 'get_object')
        urlretrieve(ps_url, local_path)

    def _is_directory(self, artifact_path:str) -> bool:
        """
        _summary_

        Args:
            artifact_path (str): relative to self.artifact_uri.  See ArtifactRepository._is_directory() for details.

        Returns:
            bool: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super()._is_directory(artifact_path)
        if not artifact_path:
            logger.debug('InfinStorArtifactRepository._is_directory: True since no artifact_path')
            return True
        if artifact_path[-1] == '/':
            logger.debug('InfinStorArtifactRepository._is_directory: True since artifact_path ends in /')
            return True
        # artifact_path is relative to self.artifact_uri and not the run's artifact root URI.  so convert it to a path relative to run's artifact root URI
        art_path_relative_to_run_root_uri = posixpath.join(self.subpath_after_runid, artifact_path) if self.subpath_after_runid else artifact_path
        ps_url = self.get_presigned_url(art_path_relative_to_run_root_uri, 'list_objects_v2')
        try:
            response = requests.get(ps_url, timeout=7200)
            if not response.ok: logger.error(f"request.method and url={response.request.method} {response.request.url}\n\nrequest.headers={response.request.headers}\n\nrequest.body={response.request.body}\n\nresponse.status_code={response.status_code}\n\nresponse.headers={response.headers}\n\nresponse.content={response.content}")
            response.raise_for_status()
        except HTTPError as http_err:   # this is requests.HTTPError and not urllib.error.HTTPError
            response = http_err.response
            logger.error('InfinStorArtifactRepository._is_directory: HTTP error occurred: '\
                    + f"request.method and url={response.request.method} {response.request.url}\n\nrequest.headers={response.request.headers}\n\nrequest.body={response.request.body}\n\nresponse.status_code={response.status_code}\n\nresponse.headers={response.headers}\n\nresponse.content={response.content}", exc_info=http_err)
            raise
        except Exception as err:
            logger.error('InfinStorArtifactRepository._is_directory: Other error occurred: ' + str(err), exc_info=err)
            raise
        root:xml.etree.ElementTree.Element = ET.fromstring(response.content)
        for prefix_elem in root.findall('./aws:CommonPrefixes/aws:Prefix', namespaces={'aws':'http://s3.amazonaws.com/doc/2006-03-01/'}):
            # list_objects_v2(), for a given prefix, may result in a match that is not an exact match of 
            # path_upto_including_runid + '/' + art_path_relative_to_run_root_uri, since it is a prefix match.
            # 
            # for example, if the prefix is 'mlflow-artifacts/user/4/4-16xxxxxx004/estimator', it may match 
            #     'mlflow-artifacts/user/4/4-16xxxxxx004/estimator.html' (in Contents) and 
            #     'mlflow-artifacts/user/4/4-16xxxxxx004/estimator_1.html' (in Contents) and 
            #      mlflow-artifacts/user/4/4-16xxxxxx004/estimator/ (in CommonPrefixes).  
            #      mlflow-artifacts/user/4/4-16xxxxxx004/estimator_dup/ (in CommonPrefixes).  
            # 
            # So check for an exact match
            # 
            # 'CommonPrefixes': [{'Prefix': 'mlflow-artifacts/username/20/20-16781922633870000000007/train/estimator/'}, {'Prefix': 'mlflow-artifacts/username/20/20-16781922633870000000007/train/estimator_dup/'}]
            # 
            # the 'Prefix' can be url encoded like: mlflow-artifacts/azuread-isstage13_user%40infinstor.com/1475/1475-16850113402480000000015/langchain_model/
            if prefix_elem.text and prefix_elem.text == quote(self.path_upto_including_runid + '/' + art_path_relative_to_run_root_uri + '/'): return True
            
        logger.debug('InfinStorArtifactRepository._is_directory: False since at no common prefix is present')
        return False

    def list_artifacts(self, path:str) -> List[FileInfo]:
        """
        _summary_

        Args:
            path (str): this is relative to artifact_uri.  See S3ArtifactRepository.list_artifacts() for details

        Returns:
            List[FileInfo]: _description_
        """
        if not self.use_presigned_url_for_mlflow:
            return super().list_artifacts(path=path)
        if not path:
            path = ''
        elif path[len(path) - 1] != '/':
            path = path + '/'
        # path is guaranteed to be a directory
        logger.info('InfinStorArtifactRepository.list_artifacts: path=' + path + ', artifact_uri=' + str(self.artifact_uri))
        (au_bucket, au_artifact_path) = our_parse_s3_uri(self.artifact_uri)
        
        # get_presigned_url() expects a prefix relative to run's artifact root URI.  but 'path' is relative to 'artifact_uri'.  Translate it now
        path_rel_run_root_uri:str = self.subpath_after_runid + '/' + path if self.subpath_after_runid else path
        ps_url = self.get_presigned_url(path_rel_run_root_uri, 'list_objects_v2')
        try:
            response = requests.get(ps_url, timeout=7200)
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error('list_artifacts: HTTP error occurred: ' + str(http_err), exc_info=http_err)
            raise
        except Exception as err:
            logger.error('list_artifacts: Other error occurred: ' + str(err), exc_info=err)
            raise
        logger.debug('InfinStorArtifactRepository.list_artifacts: resp=' + str(response.content))
        root = ET.fromstring(response.content)
        infos=[]
        for child in root:
            if (child.tag.endswith('CommonPrefixes')):
                for child1 in child:
                    fp = unquote(str(child1.text))
                    self._verify_listed_object_contains_artifact_path_prefix(
                        listed_object_path=fp, artifact_path=au_artifact_path
                    )
                    fp1 = fp[len(au_artifact_path)+1:]
                    fp2 = fp1.rstrip('/')
                    infos.append(FileInfo(fp2, True, None))
            elif (child.tag.endswith('Contents')):
                filesize = 0
                filename = None
                for child1 in child:
                    if child1.tag.endswith('Key'):
                        filename = child1.text
                    elif child1.tag.endswith('Size'):
                        filesize = int(child1.text)
                if filename:
                    fp = unquote(str(filename))
                    self._verify_listed_object_contains_artifact_path_prefix(
                        listed_object_path=fp, artifact_path=au_artifact_path
                    )
                    fp1 = fp[len(au_artifact_path)+1:]
                    fp2 = fp1.rstrip('/')
                    fp3 = fp2.lstrip('/')
                    infos.append(FileInfo(fp3, False, filesize))
        return infos

    def get_presigned_url(self, prefix:str, method:str, /, num_of_chunks:int = None, 
                          comp_multi_upload:CompleteMultiPartUploadReq = None, upload_id:str=None) -> Union[str, CreateMultiPartUploadResp]:
        """
        See below: not only returns a presigned url but can also return other strings and object instances.

        Args:
            prefix (str): prefix is relative to the run's artifact root URI.
            method (str): s3 method such as get_object | 'put_object' | 'list_objects_v2' | 'create_multipart_upload' | 'complete_multipart_upload' | 'abort_multipart_upload'

        Returns:
            Union[str, CreateMultiPartUploadResp]: returns a presigned url for method=get_object|put_object|list_objects_v2; returns the ETag for method=complete_multipart_upload; returns CreateMultiPartUploadResp for method=create_multipart_upload
        """
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            if attempt == 0:
                force = False
            else:
                logger.error('get_presigned_url: retrying')
                force = True
            attempt = attempt + 1
            token, service = get_token(builtins.region, force)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': token
                }
            url = 'https://' + builtins.mlflowserver\
                    + '/Prod/2.0/mlflow/artifacts/getpresignedurl'\
                    + '?run_id=' + self.this_run_id\
                    + '&path=' + quote(prefix)\
                    + '&method=' + method
            if num_of_chunks: url += '&num_of_chunks=' + str(num_of_chunks)            
            if comp_multi_upload:
                # convert to json string
                comp_multi_upload:str = jsons.dumps(comp_multi_upload)
                # urlencode the json
                post_contents = quote_plus(comp_multi_upload)
            else:
                post_contents = None
            if upload_id: url += "&upload_id=" + upload_id
                
            try:
                if post_contents:
                    response = requests.post(url, headers=headers, data=post_contents)
                else:
                    response = requests.get(url, headers=headers)
                response.raise_for_status()
            except HTTPError as http_err:
                logger.error('get_presigned_url(): HTTP error occurred: ' + str(http_err), exc_info=http_err)
                # if this is the last iteration of retrying, raise the exception; 'attempt' has already been incremented above, so comparision is >=, even though 'attempt' is zero based
                if attempt >= max_attempts: raise
            except Exception as err:
                logger.error('get_presigned_url(): Other error occurred: ' + str(err), exc_info=err)
                # if this is the last iteration of retrying, raise the exception; 'attempt' has already been incremented above, so comparision is >=, even though 'attempt' is zero based
                if attempt >= max_attempts: raise
            if 'Login expired. Please login again' in response.text:
                continue
            
            js = response.json()
            retval:Union[str, CreateMultiPartUploadResp]=None
            if method in ('get_object', 'put_object', 'list_objects_v2', 'complete_multipart_upload', 'abort_multipart_upload'):
                retval = js['presigned_url']
            elif method == "create_multipart_upload" or method == 'refresh_multipart_upload':
                # deserialze to CreateMultiPartUploadResp.  we need the <object> from { "presigned_url": <object> }                
                retval = jsons.loads(jsons.dumps(js['presigned_url']), CreateMultiPartUploadResp)
            else:
                logger.error(f'get_presigned_url(): Unknown method={method}')
            
            return retval
        logger.error('get_presigned_url: Tried twice. Giving up')
        return None
