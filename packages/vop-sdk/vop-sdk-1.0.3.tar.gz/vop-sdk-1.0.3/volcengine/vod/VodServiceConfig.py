# coding:utf-8

from __future__ import print_function

import threading
from zlib import crc32

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

ServiceVersion20220415 = "2022-04-15"


class VodServiceConfig(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = VodServiceConfig.get_service_info(region)
        self.api_info = VodServiceConfig.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(VodServiceConfig, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("vod.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'vod', 'cn-north-1'), 60, 60),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            # 播放
            "GetPlayInfo": ApiInfo("GET", "/", {"Action": "GetPlayInfo", "Version": ServiceVersion20220415}, {}, {}),
            "GetAllPlayInfo": ApiInfo("GET", "/", {"Action": "GetAllPlayInfo", "Version": ServiceVersion20220415}, {}, {}),
            "GetPrivateDrmPlayAuth": ApiInfo("GET", "/", {"Action": "GetPrivateDrmPlayAuth", "Version": ServiceVersion20220415}, {}, {}),
            "GetHlsDecryptionKey": ApiInfo("GET", "/", {"Action": "GetHlsDecryptionKey", "Version": ServiceVersion20220415}, {}, {}),
            "GetPlayInfoWithLiveTimeShiftScene": ApiInfo("GET", "/", {"Action": "GetPlayInfoWithLiveTimeShiftScene", "Version": ServiceVersion20220415}, {}, {}),
            # 上传
            "UploadMediaByUrl": ApiInfo("GET", "/", {"Action": "UploadMediaByUrl", "Version": ServiceVersion20220415}, {}, {}),
            "QueryUploadTaskInfo": ApiInfo("GET", "/", {"Action": "QueryUploadTaskInfo", "Version": ServiceVersion20220415}, {}, {}),
            "ApplyUploadInfo": ApiInfo("GET", "/", {"Action": "ApplyUploadInfo", "Version": ServiceVersion20220415}, {}, {}),
            "CommitUploadInfo": ApiInfo("GET", "/", {"Action": "CommitUploadInfo", "Version": ServiceVersion20220415}, {}, {}),
            # 媒资
            "UpdateMediaInfo": ApiInfo("GET", "/", {"Action": "UpdateMediaInfo", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateMediaPublishStatus": ApiInfo("GET", "/", {"Action": "UpdateMediaPublishStatus", "Version": ServiceVersion20220415}, {}, {}),
            "GetMediaInfos": ApiInfo("GET", "/", {"Action": "GetMediaInfos", "Version": ServiceVersion20220415}, {}, {}),
            "GetRecommendedPoster": ApiInfo("GET", "/", {"Action": "GetRecommendedPoster", "Version": ServiceVersion20220415}, {}, {}),
            "DeleteMedia": ApiInfo("GET", "/", {"Action": "DeleteMedia", "Version": ServiceVersion20220415}, {}, {}),
            "DeleteTranscodes": ApiInfo("GET", "/", {"Action": "DeleteTranscodes", "Version": ServiceVersion20220415}, {}, {}),
            "GetMediaList": ApiInfo("GET", "/", {"Action": "GetMediaList", "Version": ServiceVersion20220415}, {}, {}),
            "GetSubtitleInfoList": ApiInfo("GET", "/", {"Action": "GetSubtitleInfoList", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateSubtitleStatus": ApiInfo("GET", "/", {"Action": "UpdateSubtitleStatus", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateSubtitleInfo": ApiInfo("GET", "/", {"Action": "UpdateSubtitleInfo", "Version": ServiceVersion20220415}, {}, {}),
            "GetAuditFramesForAudit": ApiInfo("GET", "/", {"Action": "GetAuditFramesForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "GetMLFramesForAudit": ApiInfo("GET", "/", {"Action": "GetMLFramesForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "GetBetterFramesForAudit": ApiInfo("GET", "/", {"Action": "GetBetterFramesForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "GetAudioInfoForAudit": ApiInfo("GET", "/", {"Action": "GetAudioInfoForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "GetAutomaticSpeechRecognitionForAudit": ApiInfo("GET", "/", {"Action": "GetAutomaticSpeechRecognitionForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "GetAudioEventDetectionForAudit": ApiInfo("GET", "/", {"Action": "GetAudioEventDetectionForAudit", "Version": ServiceVersion20220415}, {}, {}),
            "CreateVideoClassification": ApiInfo("GET", "/", {"Action": "CreateVideoClassification", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateVideoClassification": ApiInfo("GET", "/", {"Action": "UpdateVideoClassification", "Version": ServiceVersion20220415}, {}, {}),
            "DeleteVideoClassification": ApiInfo("GET", "/", {"Action": "DeleteVideoClassification", "Version": ServiceVersion20220415}, {}, {}),
            "ListVideoClassifications": ApiInfo("GET", "/", {"Action": "ListVideoClassifications", "Version": ServiceVersion20220415}, {}, {}),
            "ListSnapshots": ApiInfo("GET", "/", {"Action": "ListSnapshots", "Version": ServiceVersion20220415}, {}, {}),
            # 转码
            "StartWorkflow": ApiInfo("GET", "/", {"Action": "StartWorkflow", "Version": ServiceVersion20220415}, {}, {}),
            "RetrieveTranscodeResult": ApiInfo("GET", "/", {"Action": "RetrieveTranscodeResult", "Version": ServiceVersion20220415}, {}, {}),
            "GetWorkflowExecution": ApiInfo("GET", "/", {"Action": "GetWorkflowExecution", "Version": ServiceVersion20220415}, {}, {}),
            # 空间管理
            "CreateSpace": ApiInfo("GET", "/", {"Action": "CreateSpace", "Version": ServiceVersion20220415}, {}, {}),
            "ListSpace": ApiInfo("GET", "/", {"Action": "ListSpace", "Version": ServiceVersion20220415}, {}, {}),
            "GetSpaceDetail": ApiInfo("GET", "/", {"Action": "GetSpaceDetail", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateSpace": ApiInfo("GET", "/", {"Action": "UpdateSpace", "Version": ServiceVersion20220415}, {}, {}),
            "UpdateSpaceUploadConfig": ApiInfo("GET", "/", {"Action": "UpdateSpaceUploadConfig", "Version": ServiceVersion20220415}, {}, {}),
            "DescribeVodSpaceStorageData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceStorageData", "Version": ServiceVersion20220415}, {}, {}),
            # 分发加速
            "ListDomain": ApiInfo("GET", "/", {"Action": "ListDomain", "Version": ServiceVersion20220415}, {}, {}),
            "CreateCdnRefreshTask": ApiInfo("GET", "/", {"Action": "CreateCdnRefreshTask", "Version": ServiceVersion20220415}, {}, {}),
            "CreateCdnPreloadTask": ApiInfo("GET", "/", {"Action": "CreateCdnPreloadTask", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnTasks": ApiInfo("GET", "/", {"Action": "ListCdnTasks", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnAccessLog": ApiInfo("GET", "/", {"Action": "ListCdnAccessLog", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnTopAccessUrl": ApiInfo("GET", "/", {"Action": "ListCdnTopAccessUrl", "Version": ServiceVersion20220415}, {}, {}),
            "DescribeVodDomainBandwidthData": ApiInfo("GET", "/", {"Action": "DescribeVodDomainBandwidthData", "Version": ServiceVersion20220415}, {}, {}),
            "DescribeVodDomainTrafficData": ApiInfo("GET", "/", {"Action": "DescribeVodDomainTrafficData", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnUsageData": ApiInfo("GET", "/", {"Action": "ListCdnUsageData", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnStatusData": ApiInfo("GET", "/", {"Action": "ListCdnStatusData", "Version": ServiceVersion20220415}, {}, {}),
            "DescribeIpInfo": ApiInfo("GET", "/", {"Action": "DescribeIpInfo", "Version": ServiceVersion20220415}, {}, {}),
            "ListCdnPvData": ApiInfo("GET", "/", {"Action": "ListCdnPvData", "Version": ServiceVersion20220415}, {}, {}),
            # 回调管理
            "AddCallbackSubscription": ApiInfo("GET", "/", {"Action": "AddCallbackSubscription", "Version": ServiceVersion20220415}, {}, {}),
            "SetCallbackEvent": ApiInfo("GET", "/", {"Action": "SetCallbackEvent", "Version": ServiceVersion20220415}, {}, {}),

        }
        return api_info

    @staticmethod
    def crc32(file_path):
        prev = 0
        for eachLine in open(file_path, "rb"):
            prev = crc32(eachLine, prev)
        return prev & 0xFFFFFFFF
