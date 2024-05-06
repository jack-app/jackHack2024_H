class authUrlResponse {
  auth_url: string;
  constructor(auth_url: string) {
    this.auth_url = auth_url;
  }
}

export default class EndPoints {
  static readonly domain = 'jack.hbenpitsu.net';

  static async _getContent(response: Response) {
    console.log('getcontent');
    const content = await response.json();
    if (!response.ok) {
      throw new Error(`Failed to get token: ${content.msg}`);
    }
    return content;
  }

  static async getTokens(): Promise<number> {
    console.log('gettoken');
    const resp = await fetch(`https://${EndPoints.domain}/getTokens`);
    return resp.status;
  }

  static async refreshTokens() {
    console.log('refresh');
    await fetch(`https://${EndPoints.domain}/refreshTokens`);
  }

  static async getAuthFlowState() {
    console.log('getflow');
    const response = await fetch(`https://${EndPoints.domain}/getAuthFlowState`);
    const content = await EndPoints._getContent(response);
    return new authUrlResponse(content.auth_url);
  }
}

class TokenGetter {
  static async startAuthentication() {
    console.log('startauth');
    await TokenGetter.openAuthWindow();
    for (;;) {
      await new Promise((resolve) => setTimeout(resolve, 1 * 1000)); //ms
      const status = await EndPoints.getTokens();
      if (status != 408) {
        break;
      }
    }
  }
  static async openAuthWindow() {
    console.log('openauthwindow');
    const response = await EndPoints.getAuthFlowState();
    window.open(response.auth_url, '_blank', 'tabname');
  }
}

export const authenticate = TokenGetter.startAuthentication;
export const refreshTokens = EndPoints.refreshTokens;
