from core.common import commoncomponent

#direct upwork account
# def login_session_new():
#     commoncomponent.login_to_application('upwork','amit@finoptis.org','Infy@123..')

#gmail account with OTP
def login_session_new():
    commoncomponent.login_to_application('upwork','phyllouser@gmail.com','phyllo@123')

#gmail account with OTP not enabled
# def login_session_new():
#     commoncomponent.login_to_application('upwork','phyllouser1@gmail.com','phyllo@123')

if __name__ == '__main__':
    login_session_new()