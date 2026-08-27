import HttpService from "./HttpService"

export const RegisterUserService = (data) => {
  const http = new HttpService()
  return http.postData("/users/register", data)
    .then((response) => {
      return response.data
    })
    .catch(err => { throw err })
}

export const LoginUserService = (credentials) => {
  const http = new HttpService()
  const accessTokenID = "access-token"
  const refreshTokenID = "refresh-token"
  
  return http.postData("/users/login", credentials)
    .then(response => {
      localStorage.setItem(accessTokenID, response.data.data.access)
      localStorage.setItem(refreshTokenID, response.data.data.refresh)
      return response.data
    })
    .catch(err => { throw err })
}

export const AuthorizeUserService = () => {
  const http = new HttpService()
  const tokenID = "access-token"
  
  return http.getData("/users/authorise", tokenID)
    .then(response => {
      return response.data
    })
    .catch(err => { throw err })
}

export const LogoutUserService = () => {
  const http = new HttpService()
  const accessTokenID = "access-token"
  const refreshTokenID = "refresh-token"
  const refreshToken = localStorage.getItem(refreshTokenID)
  return http.postData(
    "/users",
    { refresh: refreshToken },
    accessTokenID,
  )
    .then((response) => {
      if (null !== localStorage.getItem(accessTokenID)) {
        localStorage.removeItem(accessTokenID)
      }
      if (null !== localStorage.getItem(refreshTokenID)) {
        localStorage.removeItem(refreshTokenID)
      }
      window.location = "/user/login"
      return response.data
    })
    .catch(err => { throw err })
}