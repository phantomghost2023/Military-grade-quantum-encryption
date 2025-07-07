
// src/frontend/frontend-app/src/api.js

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export const fetchData = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, options);
    if (!response.ok) {
      let errorData = {};
      try {
        errorData = await response.json();
      } catch (e) {
        // If response is not JSON, use a generic error message
        errorData = { message: `HTTP error! status: ${response.status}`, error_code: `HTTP_${response.status}` };
      }
      throw new Error(JSON.stringify(errorData));
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    // Re-throw the error to be handled by the calling component
    throw error;
  }
};

// Example usage:
// import { fetchData } from './api';
//
// fetchData('some-resource')
//   .then(data => console.log(data))
//   .catch(error => console.error(error));
