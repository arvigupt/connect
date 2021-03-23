from core.common import commoncomponent
import mintotp

def login_to_application():
    commoncomponent.go_to('gmail', True, 'url')
    result = commoncomponent.enter_username_password('pritam@spinningjenny.net', 'gnon*RHIG9hu4blas')
    if result == True:
        commoncomponent.enter_otp(mintotp.totp('bo3macr3ml7vtxw7vg2nn4vtql7uyq6t'))

# def login_new_login_session_to_application():
#     commoncomponent.go_to('gmail', True, 'url')
#     result = commoncomponent.enter_username_password('pritam@spinningjenny.net', 'gnon*RHIG9hu4blas')
#     if result == True:
#         commoncomponent.enter_otp(mintotp.totp('bo3macr3ml7vtxw7vg2nn4vtql7uyq6t'))
#     commoncomponent.go_to('gmail', False, 'homepageurl')
#     commoncomponent.enter_username_password('pritam@spinningjenny.net', 'gnon*RHIG9hu4blas')


def login_new_login_session_to_application1():
    commoncomponent.go_to('gmail', True, 'url')
    result = commoncomponent.enter_username_password('Hello@getphyllo.com', 'Phyllo@123')
    if result == True:
        commoncomponent.enter_otp(mintotp.totp('js6aegv5sm5mqw3gguumw3aoue7atphe'))
    commoncomponent.go_to('gmail', False, 'homepageurl')
    commoncomponent.enter_username_password('automationuser1@spinningjenny.net', 'Auto1#2o19')

    value = commoncomponent.navigatetoDestinationAndPerform('gmail','homepage','contactpage')
    print(value)

def login_session_new():
    commoncomponent.login_to_application('upwork','amit@finoptis.org','Infy@123..')


if __name__ == '__main__':
    login_session_new()