# USER
SIGNUP_USER = '''
mutation SignupUser(
    $email: String!,
    $password: String!
){
    signupUser(
        email: $email,
        password: $password
    ){
        email
        firstName
        lastName
    },
    tokenAuth(
        email: $email,
        password: $password
    ){
        token
    }   
}
'''

TOKEN_AUTH = '''
mutation TokenAuth(
    $email: String!, 
    $password: String!
){
    tokenAuth(
        email: $email, 
        password: $password
    ){
        token
    }
}
'''

CURRENT_USER = '''
query CurrentUser{
    currentUser{
        email
        dateJoined
    }
}
'''

ALL_USER = '''
query AllUser{ 
    allUsers{
        email
    }
}
'''
