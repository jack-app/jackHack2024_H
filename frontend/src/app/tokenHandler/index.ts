class authUrlResponse {
  auth_url: string;
  constructor(auth_url: string) {
    this.auth_url = auth_url;
  }
}

export default class EndPoints {
  static readonly domain = 'jack.hbenpitsu.net';

  static async _getContent(response: Response) {
    const content = await response.json();
    if (!response.ok) {
      throw new Error(`Failed to get token: ${content.msg}`);
    }
    return content;
  }

  static async getTokens(): Promise<number> {
    const resp = await fetch(`https://${EndPoints.domain}/getTokens`);
    return resp.status;
  }

  static async refreshTokens() {
    await fetch(`https://${EndPoints.domain}/refreshTokens`);
  }

  static async getAuthFlowState() {
    const response = await fetch(`https://${EndPoints.domain}/getAuthFlowState`);
    const content = await EndPoints._getContent(response);
    return new authUrlResponse(content.auth_url);
  }
}

class TokenGetter {
  static async startAuthentication() {
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
    const response = await EndPoints.getAuthFlowState();
    window.open(response.auth_url);
  }
}

export const authenticate = TokenGetter.startAuthentication;
export const refreshTokens = EndPoints.refreshTokens;
