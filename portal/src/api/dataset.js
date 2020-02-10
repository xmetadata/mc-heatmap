import request from '@/utils/request'

export function getDataset(data) {
  return request({
    url: '/dataset',
    method: 'post',
    data
  })
}
