import alibabacloud_oss_v2 as oss

class AliyunFileService:
    def __init__(self,access_key,access_key_secret,bucket_name,region_id):
        self.bucket_name = bucket_name
        self.region_id = region_id
        self.client = oss.Client(
            access_key_id=access_key,
            access_key_secret=access_key_secret,
            region_id=region_id
        )
    def UploadFile(self,file,fileName):
        # 实现向阿里云的cos上传文件
        # file: 可以是文件路径或文件对象
        # fileName: 上传到OSS后的文件名
        try:
            # 如果 file 是文件路径
            if isinstance(file, str):
                with open(file, 'rb') as f:
                    self.client.put_object(
                        bucket_name=self.bucket_name,
                        key=fileName,
                        body=f
                    )
            else:
                # file 是文件对象
                self.client.put_object(
                    bucket_name=self.bucket_name,
                    key=fileName,
                    body=file
                )
            # 返回文件的 OSS 访问路径
            file_url = f"https://{self.bucket_name}.oss-{self.region_id}.aliyuncs.com/{fileName}"
            return file_url
        except Exception as e:
            print(f"上传失败: {e}")
            return False