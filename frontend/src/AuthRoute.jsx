import React, { useEffect, } from "react"
import { Outlet, Navigate, } from "react-router"
import { useSelector, useDispatch, } from "react-redux"
import { authorise, } from "./redux/actions/authActions"

const AuthRoute = ({ redirectPath, }) => {
  const dispatch = useDispatch()
  const state = useSelector(state => ({
    auth: state.auth,
  }))

  useEffect(() => {
    dispatch(authorise())
  }, [])

  if (
    state.auth.loading || 
    (
      null === state.auth.data &&
      null === state.auth.error
    )
  ) {
    return null
  }

  const accessTokenID = "access-token"
  const refreshTokenID = "refresh-token"
  const userStorage = localStorage.getItem(accessTokenID)
  const refreshStorage = localStorage.getItem(refreshTokenID)
  if (
    state.auth.error ||
    null === userStorage ||
    null === refreshStorage
  ) {
    if (null !== userStorage) {
      localStorage.removeItem(accessTokenID)
    }
    if (null !== refreshStorage) {
      localStorage.removeItem(refreshTokenID)
    }
    if (redirectPath) {
      return <Navigate to={redirectPath}/>
    } else {
      return <Navigate to={"/user/login"}/>
    }
  }

  return <Outlet/>
}

export default AuthRoute