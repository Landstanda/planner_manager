# Development Setup Guide

This guide outlines the recommended setup for developing the Daily Planner AI Agent, focusing on a hybrid approach: local development for speed and iteration, and deployment to Fly.io for testing in a production-like environment.

## 1. Local Development (Next.js Frontend)

The Next.js frontend application (`nextjs_app`) should be developed locally for the fastest feedback loop.

### Prerequisites:
*   Node.js (version specified in `nextjs_app/Dockerfile`, currently Node 18)
*   npm or yarn

### Environment Variables:
Your local Next.js application will need to communicate with the n8n service running on Fly.io. To enable this, you'll use a local environment file.

1.  **Create `.env.local`:**
    In the `nextjs_app` directory, create a file named `.env.local`. This file is gitignored, so your secrets will not be committed to the repository.

2.  **Populate `.env.local`:**
    Add the following variables to your `nextjs_app/.env.local` file, replacing the placeholder values with your actual n8n application URL and the API key you will configure for your n8n webhooks:

    ```env
    N8N_BASE_URL=https://your-n8n-app-name.fly.dev
    N8N_WEBHOOK_API_KEY=your_actual_n8n_webhook_api_key

    # You can add other local-only environment variables here if needed
    # NEXT_PUBLIC_SOME_CONFIG=some_value 
    ```
    *   Replace `https://your-n8n-app-name.fly.dev` with the actual URL of your deployed n8n application on Fly.io (e.g., `https://aphro-email-manager.fly.dev`).
    *   Replace `your_actual_n8n_webhook_api_key` with the secret key you will configure in your n8n webhook nodes for authentication.

    Refer to `nextjs_app/.env.example` for a template of expected environment variables.

### Running the Local Development Server:
1.  Navigate to the `nextjs_app` directory:
    ```bash
    cd nextjs_app
    ```
2.  Install dependencies (if you haven't already):
    ```bash
    npm install
    # or
    # yarn install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    # or
    # yarn dev
    ```
    This will typically start the Next.js app on `http://localhost:3000`.

## 2. n8n Workflow Development

*   n8n workflows are developed directly within your n8n instance running on Fly.io.
*   Remember to export your workflow JSON files periodically for version control (as outlined in `task.md`).
*   When configuring webhooks in n8n that your Next.js app will call, ensure you set up authentication (e.g., Header Auth) and use the same API key in your Next.js app's `N8N_WEBHOOK_API_KEY` environment variable.

## 3. Testing Full Integrations (Deploying to Fly.io)

For testing how your Next.js application behaves in a production-like environment and for end-to-end testing with the live n8n instance:

1.  **Ensure your code is committed to Git.**
2.  **Deploy the Next.js app (`chief-of-staff`) to Fly.io:**
    From your workspace root directory:
    ```bash
    flyctl deploy --config ./nextjs_app/fly.toml 
    ```
    Or, if you are in the `nextjs_app` directory:
    ```bash
    flyctl deploy
    ```
    *(Note: Ensure you have the Fly CLI installed and are logged in.)*

3.  **Set Secrets in Fly.io:**
    Make sure that the necessary secrets (like `N8N_BASE_URL` and `N8N_WEBHOOK_API_KEY`) are set in the Fly.io dashboard for your `chief-of-staff` Next.js application. These will be injected as environment variables at runtime.

This hybrid approach allows for rapid local UI and feature development while ensuring robust testing in an environment that mirrors production. 