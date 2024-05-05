export default class TokenGetter {
  static readonly domain = 'jack.hbenpitsu.net';

  static async getToken() {
    const response = await fetch(`https://${TokenGetter.domain}/getTokens`);
    if (!response.ok) {
      throw new Error('Failed to get token');
    }
  }

  static async getRefreshToken() {
    const response = await fetch(`https://${TokenGetter.domain}/getRefreshTokens`);
    if (!response.ok) {
      throw new Error('Failed to get refresh token');
    }
  }

  static async getAuthFlowState() {
    const response = await fetch(`https://${TokenGetter.domain}/getAuthFlowState`);
    if (!response.ok) {
      throw new Error('Failed to get auth flow state');
    }
  }

  static async getOAuth2callback() {
    const response = await fetch(`https://${TokenGetter.domain}/oauth2callback`);
    if (!response.ok) {
      throw new Error('Failed to get OAuth2 callback');
    }
  }
}
