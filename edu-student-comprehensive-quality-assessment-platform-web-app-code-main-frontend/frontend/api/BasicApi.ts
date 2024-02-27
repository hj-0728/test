import http from '../http';
import { MessageCarrier } from "@/model/Basic.model";

const defHttp = {
  async get<T>(url: string, params?: any): Promise<MessageCarrier<T>> {
    try {
      const response = await http.get(url, {searchParams: params});
      return await response.json();
    } catch (error) {
      console.error('Error during GET request:', error);
      throw error;
    }
  },

  async post<T>(url: string, json?: any, body?: any): Promise<MessageCarrier<T>> {
    try {
      const options: { json?: any, body?: any } = {}
      if (json) {
        options.json = json;
      }
      if (body) {
        options.body = body;
      }
      const response = await http.post(url, options);
      return await response.json();
    } catch (error) {
      console.error('Error during POST request:', error);
      throw error;
    }
  },
};

export default defHttp;
