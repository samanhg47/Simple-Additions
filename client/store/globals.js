import Axios from 'axios'

export const BASE_URL =
  process.env.NODE_ENV === 'production'
    ? `${window.location.origin}/api`
    : 'http://localhost:5000/api'

export const Client = Axios.create({ baseURL: BASE_URL })

Client.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    const adminAuth = localStorage.getItem('Admin')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      config.headers['Admin'] = adminAuth
    }
    return config
  },
  error => Promise.reject(error)
)
export default Client
