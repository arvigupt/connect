from core.common import commoncomponent
from core.common.repository import data_platform
from core.common.repository import dp_applicant_login_info

login_status = 'login_status'

def start_login():
    tenant_id = 'fc14a17d-0667-4bd6-856e-b4aaec68984c'
    applicant_id = 'c1af9c06-2c9e-4de0-9745-cbf36bc1be0f'
    dp_name = input("Enter data platform name: ")
    data_platform_id = data_platform.fetch_data_platform_id(dp_name)
    applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
    applicant_username = ""
    applicant_pwd = ""
    applicant_otp = ""

    if applicant_login_info == None:
        applicant_username = input("Enter username: ")
        applicant_pwd = input("Enter password: ")
        dp_applicant_login_info.insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
        dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, '', "none")
        applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
    elif applicant_login_info[login_status] == None or applicant_login_info[login_status] == "none":
        applicant_username = input("Enter username: ")
        applicant_pwd = input("Enter password: ")
    elif applicant_login_info[login_status] == "in-progress" :
        applicant_otp = input("Enter OTP: ")
    elif applicant_login_info[login_status] == "completed":
        option = input("Previous login operation is completed. Do you want to start again (Y/N): ")
        if option == "y" or option == "Y":
            dp_applicant_login_info.delete_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
            applicant_username = input("Enter username: ")
            applicant_pwd = input("Enter password: ")
            dp_applicant_login_info.insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
            dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, '', "none")
            applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id,
                                                                                         applicant_id)
        else:
            print("Operation completed successfully.")
            exit(1)

    commoncomponent.login_to_application(tenant_id, data_platform_id, applicant_id, applicant_username, applicant_pwd,
                                         applicant_otp, applicant_login_info)


if __name__ == '__main__':
    start_login()