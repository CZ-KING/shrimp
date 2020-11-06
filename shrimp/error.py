class ErrorCode:
    sucess = 0
    invalid_arguments = 1
    sign_error = 2
    captcha_invalid = 3
    captcha_expired = 4
    user_exists = 5
    user_not_exists = 6
    database_error = 7
    request_denied = 8
    request_frequently = 9
    request_invalid = 10


MESSAGE = {
    ErrorCode.sucess:"成功",
    ErrorCode.invalid_arguments:"参数无效",
    ErrorCode.sign_error:"签名错误",
    ErrorCode.captcha_invalid:"验证码无效",
    ErrorCode.captcha_expired:"验证码过期",
    ErrorCode.user_exists:"用户已存在",
    ErrorCode.user_not_exists:"用户不存在",
    ErrorCode.database_error:"数据库错误",
    ErrorCode.request_denied:"请求拒绝",
    ErrorCode.request_frequently:"请求频繁",
    ErrorCode.request_invalid:"请求无效",

}