from dotenv import load_dotenv
import os

# Pipeline input and output types.
INPUT_NODE_TYPES = ['text', 'file']
OUTPUT_NODE_TYPES = ['text', 'file']

# VectorStore parameters.
VECTORSTORE_DEFAULT_CHUNK_SIZE = 400
VECTORSTORE_DEFAULT_CHUNK_OVERLAP = 0

# Node-specific parameters.
# TODO: this might be redundant (e.g. llm-openai-node.js)
# Map of LLMs to token limits
SUPPORTED_OPENAI_LLMS = {
    'gpt-3.5-turbo': 4096,
    'gpt-3.5-turbo-16k': 16384,
    'gpt-4': 8192,
    'gpt-4-32k': 32768
}
SUPPORTED_ANTHROPIC_LLMS = {'claude-v2': 100000}
# Map of image gen models to possible sizes (in both dimensions; if in the 
# future non-square images can be generated we'll update this), and # of
# possible images to generate
SUPPORTED_IMAGE_GEN_MODELS = {
    'DALL·E 2': ([256, 512, 1024], list(range(1, 5))),
    'Stable Diffusion XL': ([512], [1])
}
SUPPORTED_SPEECH_TO_TEXT_MODELS = ['OpenAI Whisper']
CHAT_MEMORY_TYPES = ['Full - Formatted', 'Full - Raw', 'Message Buffer', 'Token Buffer']

# Specifications of the input names that dataloader nodes expect. 
# A dictionary that maps the dataloader type to a list of expected input names
# and the particular task name assigned to the node in Mongo.
DATALOADER_PARAMS = {
    'File': {
        'input_names': ['file'],
        'task_name': 'load_file',
    },
    'CSV Query': {
        'input_names': ['query', 'csv'],
        'task_name': 'query_csv',
    },
    'URL': {
        'input_names': ['url'],
        'task_name': 'load_url',
    },
    'Wikipedia': {
        'input_names': ['query'],
        'task_name': 'load_wikipedia',
    },
    'YouTube': {
        'input_names': ['url'],
        'task_name': 'load_youtube',
    },
    'Arxiv': {
        'input_names': ['query'],
        'task_name': 'load_arxiv',
    },
    'SerpAPI': {
        'input_names': ['apiKey', 'query'],
        'task_name': 'load_serpapi',
    },
    'Git': {
        'input_names': ['repo'], 
        'task_name': 'load_git'
    },
    'Notion': {
        'input_names': ['token', 'database'],
        'task_name': 'load_notion'
    },
    'Confluence': {
        'input_names': ['username', 'apiKey', 'url'],
        'task_name': 'load_confluence'
    }
}

# Specifications of the input names that integration nodes expect. 
# A doubly-nested dictionary. In the first level, we map the integration node type (as stored in the object's type field in the Mongo integrations table) to
# a dict of supported functions for that integration (as will be described in 
# the node's data.function.name field in the Mongo pipeline table). In the 
# second level, each function name is mapped to its task/display name and its
# input/output details. Note: the function name should be added to the resulting 
# object value's name field if working with Mongo.

# TODO: This is analogous to app/src/reactflow/nodes/integration-schema.js, I 
# wonder if we could combine them somehow.
INTEGRATION_PARAMS = {
    'Salesforce': {
        'run_sql_query': {
            'taskName': 'salesforce.run_sql_query',
            'displayName': 'Run SQL Query',
            'inputs': [{ 
                'name': 'sql_query', 
                'displayName': 'SQL Query', 
                'multiInput': True 
            }],
            'outputs': [{ 'name': 'output', 'displayName': 'Output'}],
            'fields': []
        },
    },
    'Google Drive': {
        'read_files': {
            'taskName': 'google_drive.read_files',
            'displayName': 'Read Files',
            'inputs': [],
            'outputs': [{ 'name': 'output', 'displayName': 'Output' }],
            'fields': []
        },
        'save_files': {
            'taskName': 'google_drive.save_files',
            'displayName': 'Save Files',
            'inputs': [
                { 'name': 'name', 'displayName': 'Name', 'multiInput': False },
                { 'name': 'files', 'displayName': 'Files', 'multiInput': True },
            ],
            'outputs': [],
            'fields': []
        },
    },
    'Microsoft': {},
    'Notion': {
        'read_data': {
            'taskName': 'notion.read_data',
            'displayName': 'Read Data',
            'inputs': [],
            'outputs': [{ 'name': 'output', 'displayName': 'Output' }],
            'fields': []
        }
    },
    'Airtable': {
        'read_tables': {
            'taskName': 'airtable.read_tables',
            'displayName': 'Read Tables',
            'inputs': [],
            'outputs': [{'name': 'output', 'displayName': 'Output'}],
            'fields': [{
                'name': 'selectedTables', 
                'displayName': 'Select Tables', 
                'type': 'button', 
                'completedValue': 'Tables Selected'
            }],
        },
    },
    'HubSpot': {
        'search_contacts': {
            'taskName': 'hubspot.search_companies',
            'displayName': 'Search Companies',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        },
        'search_companies': {
            'taskName': 'hubspot.search_companies',
            'displayName': 'Search Companies',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        },
        'search_deals': {
            'taskName': 'hubspot.search_deals',
            'displayName': 'Search Deals',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        }
    },
    'SugarCRM': {
        'get_records': {
            'taskName': 'sugar_crm.get_records',
            'displayName': 'Get Records',
            'inputs': [
                {'name': 'module', 'displayName': 'Module', 'multiInput': False},
                {'name': 'filter', 'displayName': 'Filter', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        }
    }
}

# Relevant API endpoints the SDK code needs. Could also refactor to get rid of
# MODE entirely.
load_dotenv()
MODE = os.environ.get('ENVIRONMENT', 'PROD')
DOMAIN = 'http://localhost:8000' if MODE != 'PROD' else 'https://api.vectorshift.ai'

API_FILE_FETCH_ENDPOINT = f'{DOMAIN}/api/files/fetch'
API_INTEGRATION_FETCH_ENDPOINT = f'{DOMAIN}/api/integrations/fetch'
API_TRANSFORMATION_FETCH_ENDPOINT = f'{DOMAIN}/api/transformations/fetch'

API_VECTORSTORE_SAVE_ENDPOINT = f'{DOMAIN}/api/vectorstores/add'
API_VECTORSTORE_FETCH_ENDPOINT = f'{DOMAIN}/api/vectorstores/fetch'
API_VECTORSTORE_LOAD_ENDPOINT = f'{DOMAIN}/api/vectorstores/load'
API_VECTORSTORE_QUERY_ENDPOINT = f'{DOMAIN}/api/vectorstores/query'
API_VECTORSTORE_LIST_VECTORS_ENDPOINT = f'{DOMAIN}/api/vectorstores/list-vectors'

API_PIPELINE_SAVE_ENDPOINT = f'{DOMAIN}/api/pipelines/add'
API_PIPELINE_FETCH_ENDPOINT = f'{DOMAIN}/api/pipelines/fetch'
API_PIPELINE_RUN_ENDPOINT = f'{DOMAIN}/api/pipelines/run'

API_AGENT_SAVE_ENDPOINT = f'{DOMAIN}/api/agents/add'
API_AGENT_FETCH_ENDPOINT = f'{DOMAIN}/api/agents/fetch'
API_AGENT_RUN_ENDPOINT = f'{DOMAIN}/api/agents/run'

API_CHATBOT_SAVE_ENDPOINT = f'{DOMAIN}/api/chatbots/add'
API_CHATBOT_FETCH_ENDPOINT = f'{DOMAIN}/api/chatbots/fetch'
API_CHATBOT_RUN_ENDPOINT = f'{DOMAIN}/api/chatbots/run'
