export interface IQiSession {
    isConnected(): boolean;
    disconnect(): void;
    service(serviceName: String): any; // Define a more specific return type if possible
    //service(serviceName: String): Promise<IQiService>; // Define a more specific return type if possible
  }

export interface IQiService {

}