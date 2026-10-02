import type {
	IAuthenticateGeneric,
	Icon,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class FlatmarkApi implements ICredentialType {
	name = 'flatmarkApi';

	displayName = 'Flatmark API';

	icon: Icon = { light: 'file:../icons/flatmark.svg', dark: 'file:../icons/flatmark.svg' };

	documentationUrl = 'https://flatmark.dev/go/n8n?to=/app/api-keys';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
			description: 'Create a key at https://flatmark.dev/go/n8n?to=/app/api-keys',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'X-API-Key': '={{$credentials.apiKey}}',
			},
		},
	};

	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.flatmark.dev',
			url: '/v1/me',
			method: 'GET',
		},
	};
}
