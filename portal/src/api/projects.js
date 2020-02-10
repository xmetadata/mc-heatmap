import request from '@/utils/request'

export function getProjectList(params) {
  return request({
    url: '/project',
    method: 'get',
    params
  })
}

export function getPorjectDetail(uuid) {
  return request({
    url: '/project/' + uuid,
    method: 'get'
  })
}

export function updateProject(data) {
  return request({
    url: '/project/' + data.uuid,
    method: 'put',
    data
  })
}

export function deleteProject(uuid) {
  return request({
    url: '/project/' + uuid,
    method: 'delete'
  })
}
