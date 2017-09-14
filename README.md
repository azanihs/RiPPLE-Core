# RiPPLE Client
Recommendation in a Personalised Peer Learning Environment
The client component of RiPPLE

# Technology Stack
* Development
    * [TypeScript](https://www.typescriptlang.org/)
    * HTML5
    * CSS3
* Software Frameworks
    * [VueJS](https://vuejs.org/)
    * [Vue-Material](https://vuematerial.github.io/#/)
    * [Bulma](https://github.com/vue-bulma/chartjs)
* Utilities
    * [Webpack](https://webpack.github.io/)
    * [av-ts](https://github.com/HerringtonDarkholme/av-ts)
    * CI?

# Getting Started
First, you need to download the project.
If you have git installed you can clone the project, otherwise you will need to manually download and extract the zip archive.

Once you have a copy of the project, you can use your favourite command-line software to navigate to your newly downloaded copy of the project and use the following commands to get started:
```
npm install
cp .env.example .env.dev
cp .env.example .env.prod
```

Next, you will need to edit the environment settings to your `dev` and `prod` environment files. This allows better interpolability between systems with different configurations. The most important thing to set is the `API_LOCATION` variable, which determines where the application will look for application data.

## Development Commands
This project comes packaged with several convenience commands

* `npm run dev`
    * Creates a local development server, and serves your files over it. When a local file is changed your project will be rebuilt incrementally and the new code injected into your web browser.
* `npm run build`
    * Optimizes your code and writes a distributable to the `./dist` directory. This should be used for the production version.
* `npm run lint`
    * Runs eslint over the codebase to ensure it meets the specified JavaScript style guide.
* `npm run unit`
    * Runs all unit tests for the project. They are located under `./test/unit/spec/`
* `npm run e2e`
    * Runs all integration tests for the project. They are located under `./test/e2e/spec/`.
	* The current webdrivers which are used are:
		* PhantomJS (runs headlessly) (Installed locally as part of `npm install`)
* `npm run test`
    * Runs all unit tests and e2e tests. It is the same as `npm run unit && npm run e2e`
