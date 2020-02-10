import request from '@/utils/request'

export function getOptions(params) {
  return request({
    url: '/options',
    method: 'get',
    params
  })
}
