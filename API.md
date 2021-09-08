AuthenticateUserLogin
LoginAndGetSessionDetails(username, password, application_id, application_version)

  TC2.asmx/AuthenticateUserLogin
    POST {'userName': , 'password': , 'ApplicationID': , 'ApplicationVersion': }

  data['SessionID'] confirmed
  response['ModuleFlags']
  response['UserInfo']
  response['Locations']['LocationInfoBasic']['LocationID']

ValidateUserCode(token, device_id, usercode)

Logout(token)

  TC2.asmx/Logout
    POST {'SessionID': }

GetPanelMetaDataAndFullStatusEx_V2(token, locationid, 0, 0, _partition_list)

  TC2.asmx/GetPanelMetaDataAndFullStatus
    POST {'SessionID': , 'LocationID':, 'LastSequenceNumber':, 'LastUpdatedTimestampTicks':, 'PartitionID': }

  data['PanelMetadataAndStatus'] confirmed
  response['ArmingState']

GetZonesListInStateEx_V1(token, locationid, _partition_list, 0)
  response['ZoneStatus']
  response['ResultCode']

GetPartitionsDetails(token, locationid, security_device_id)
  response['PartitionsInfoList']

ArmSecuritySystemPartitionsV1(token, locationid, security_device_id, arm_type, 'usercode', partition_list)

  TC2.asmx/ArmSecuritySystem
    POST { 'SessionID':, 'LocationID':, 'DeviceID':, 'ArmType':, 'UserCode': }

  response['ResultCode']

DisarmSecuritySystemPartitionsV1(token, locationid, security_device_id, 'usercode', partition_list)

  TC2.asmx/DisarmSecuritySystem
    POST { 'SessionID':, 'LocationID':, 'DeviceID':, 'UserCode': }

  response['ResultCode']

Bypass(token, locationid, security_device_id, zoneid, 'usercode')
  response['ResultCode']

CustomArmSecuritySystem(token, locationid, security_device_id, armtype, 'usercode', SETTINGS)
  response['ResultCode']

GetCustomArmSettings(token, locationid, security_device_id)

GetPartitionsDetails is only way to get SecurityPanelPartitionsResults
SecurityPanelPartitionsResults is a sequence of 0 or 1 PartitionsInfoList
PartitionsInfoList is an ArrayOfPartitionDetails

PanelBaseInfoV1 is a sequence of 0 or 1 ArrayOfPartitionDetails
