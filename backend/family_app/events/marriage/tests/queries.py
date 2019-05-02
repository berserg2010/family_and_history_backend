# MARRIAGE
ALL_MARRIAGE = '''
query AllMarriage($idFamily: ID){
    allMarriage(idFamily: $idFamily){
        id
    }
}
'''

MARRIAGE = '''
query Marriage($id: ID!){
    marriage(id: $id){
        id
    }
}
'''

SAVE_MARRIAGE = '''
mutation SaveMarriage(
    $data: MarriageInput
){
    saveMarriage(
        data: $data
    ){
        status
        formErrors
        marriage{
            id
        }
    }
}
'''

DELETE_MARRIAGE = '''
mutation DeleteMarriage($id: ID!){
    deleteMarriage(id: $id){
        status
        id
    }
}
'''

LIKE_MARRIAGE = '''
mutation LikeMarriage($id: ID!, $email: String!){
    likeMarriage(
        id: $id,
        email: $email,
    ){
        marriage{
            likes
        }
    }
}
'''
