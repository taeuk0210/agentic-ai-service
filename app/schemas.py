from pydantic import BaseModel

from openai.types.chat import ChatCompletion


class VerifyUserRequest(BaseModel):
    pass


class VerifyUserResponse(BaseModel):
    pass


class SetHistoryRequest(BaseModel):
    pass


class SetHistoryResponse(BaseModel):
    pass


class GetHistoryRequest(BaseModel):
    pass


class GetHistoryResponse(BaseModel):
    pass


class ClassifyIntentRequest(BaseModel):
    pass


class ClassifyIntentResponse(BaseModel):
    pass


class GenerateAnswerRequest(BaseModel):
    pass


class GenerateAnswerResponse(BaseModel):
    pass


class TrainRequest(BaseModel):
    pass


class TrainResponse(BaseModel):
    pass


class EvaluateRequest(BaseModel):
    pass


class EvaluateResponse(BaseModel):
    pass


class GetRequest(BaseModel):
    pass


class GetResponse(BaseModel):
    pass


class SetRequest(BaseModel):
    pass


class SetResponse(BaseModel):
    pass


class DeleteRequest(BaseModel):
    pass


class DeleteResponse(BaseModel):
    pass


class EmbeddingRequest(BaseModel):
    pass


class EmbeddingResponse(BaseModel):
    pass


class CreateCollectionRequest(BaseModel):
    pass


class CreateCollectionResponse(BaseModel):
    pass


class DeleteCollectionRequest(BaseModel):
    pass


class DeleteCollectionResponse(BaseModel):
    pass


class UpsertVectorsRequest(BaseModel):
    pass


class UpsertVectorsResponse(BaseModel):
    pass


class QueryVectorsRequest(BaseModel):
    pass


class QueryVectorsResponse(BaseModel):
    pass


class DeleteVectorsRequest(BaseModel):
    pass


class DeleteVectorsResponse(BaseModel):
    pass


class GenerateRequest(BaseModel):
    pass


class GenerateResponse(BaseModel):
    pass


class CreateBucketRequest(BaseModel):
    pass


class CreateBucketResponse(BaseModel):
    pass


class DeleteBucketRequest(BaseModel):
    pass


class DeleteBucketResponse(BaseModel):
    pass


class UploadFileRequest(BaseModel):
    pass


class UploadFileResponse(BaseModel):
    pass


class DownloadFileRequest(BaseModel):
    pass


class DownloadFileResponse(BaseModel):
    pass


class DeleteFileRequest(BaseModel):
    pass


class DeleteFileResponse(BaseModel):
    pass
