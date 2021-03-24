from core.common import commoncomponent

def login_session_new():
    dp_name = input("Enter data platform name: ")
    applicant_username = input("Enter username: ")
    applicant_pwd = input("Enter password: ")
    commoncomponent.login_to_application(dp_name, applicant_username, applicant_pwd)

if __name__ == '__main__':
    login_session_new()