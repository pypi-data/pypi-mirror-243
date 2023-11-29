import { IQiSession } from './iqisession'

interface Deferred {
    resolve: (value: unknown) => void;
    reject: (reason?: any) => void;
    __cbi?: CallbackInfo;
}

interface CallbackInfo {
    obj: any;
    signal: string;
    cb: (...args: any[]) => void;
}

export class WebsocketQiSession implements IQiSession {
    private socket: WebSocket;
    private _dfd: Deferred[];
    //private _sigs: Array<Record<string, (...args: any[]) => void>>;
    private _sigs: Record<string, Record<string, (...args: any[]) => void>>[];
    private _idm: number;
    private _isConnected: boolean = false

    constructor(
        host: string,
        port: number = 8443,
        connected?: () => void,
        disconnected?: () => void) {
      var hostAndPort = `${host ? host : window.location.host}:${port}`
      console.log(`Connecting via Websocket Qimessaging, which will only work if WebsocketQimessaging is installed on the robot`);
      console.log(`On first connection, you may need to manually navigate to https://${hostAndPort} and accept the certificate.`);
      console.log(`This is unfortunately needed because the NAO has no public IP address and domain so has no ways of having a valid certificate.`);
      this.socket = new WebSocket(`wss://${hostAndPort}`);

      this._dfd = [];
      this._sigs = [];
      this._idm = 0;

      this.socket.onopen = () => {
        this._isConnected = true
        if (connected) {
          connected();
        }
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Handle the received data
        this.handleMessage(data);
      };

      this.socket.onclose = () => {
        this._isConnected = false
        for (const idm in this._dfd) {
          this._dfd[idm].reject(`Call ${idm} canceled: disconnected`);
          delete this._dfd[idm];
        }

        if (disconnected) {
          disconnected();
        }
      };

      this.service = this.createMetaCall("ServiceDirectory", "service");
    }
    isConnected(): boolean {
        return this._isConnected;
    }
    disconnect(): void {
        this.socket.close();
        //throw new Error('Method not implemented.');
    }

    private handleMessage(data: any): void {
        if (data.name === 'reply') {
          const idm = data.args.idm;
          if (data.args.result !== null && data.args.result.metaobject !== undefined) {
            const o: any = {};
            o.__MetaObject = data.args.result.metaobject;
            const pyobj = data.args.result.pyobject;
            this._sigs[pyobj] = {};

            const methods = o.__MetaObject.methods;
            for (const i in methods) {
              const methodName = methods[i].name;
              o[methodName] = this.createMetaCall(pyobj, methodName);
            }

            const signals = o.__MetaObject.signals;
            for (const i in signals) {
              const signalName = signals[i].name;
              o[signalName] = this.createMetaSignal(pyobj, signalName, false);
            }

            const properties = o.__MetaObject.properties;
            for (const i in properties) {
              const propertyName = properties[i].name;
              o[propertyName] = this.createMetaSignal(pyobj, propertyName, true);
            }

            this._dfd[idm].resolve(o);
          } else {
            const cbi = this._dfd[idm].__cbi;
            //if (this._dfd[idm].__cbi !== undefined) {
            if (cbi !== undefined) {
                this._sigs[cbi.obj][cbi.signal][data.args.result] = cbi.cb;
            }
            this._dfd[idm].resolve(data.args.result);
          }
          delete this._dfd[idm];
        } else if (data.name === 'error') {
          if (data.args.idm !== undefined) {
            this._dfd[data.args.idm].reject(data.args.result);
            delete this._dfd[data.args.idm];
          }
        } else if (data.name === 'signal') {
          const res = data.args.result;
          const callback = this._sigs[res.obj][res.signal][res.link];
          if (callback !== undefined) {
            callback.apply(this, res.data);
          }
        }
      }

    private createMetaCall(obj: any, member: string, data?: any): (...args: any[]) => Promise<any> {
      return (...args: any[]) => {
        const idm = ++this._idm;
        const promise = new Promise<any>((resolve, reject) => {
          this._dfd[idm] = { resolve, reject };
        });
        if (args[0] === "connect") {
          this._dfd[idm].__cbi = data;
        }
        this.socket.send(JSON.stringify({ idm, params: { obj, member, args } }));
        return promise;
      }
    }

    private createMetaSignal(obj: any, signal: string, isProperty: boolean): any {
      const s: any = {};
      this._sigs[obj] = this._sigs[obj] || {};
      this._sigs[obj][signal] = {};
      s.connect = (cb: (...args: any[]) => void) => {
        return this.createMetaCall(obj, signal, { obj, signal, cb })("connect");
      }
      s.disconnect = (l: any) => {
        delete this._sigs[obj][signal][l];
        return this.createMetaCall(obj, signal)("disconnect", l);
      }

      if (!isProperty) {
        return s;
      }

      s.setValue = (...args: any[]) => {
        return this.createMetaCall(obj, signal)(...["setValue", ...args]);
      }
      s.value = () => {
        return this.createMetaCall(obj, signal)("value");
      }
      return s;
    }

    public service: (...args: any[]) => Promise<any>;
  }
