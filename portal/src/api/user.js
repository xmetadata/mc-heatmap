import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/userinfo',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
