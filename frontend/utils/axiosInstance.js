// CREATING AXIOS INSTANCE

import { BASE_URL } from "./apiPaths";

const api = axios.create({
  baseUrl: BASE_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});



export default api