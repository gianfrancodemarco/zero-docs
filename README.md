# ZeroDocs 📚

![ZeroDocs](hero.jpg)

ZeroDocs is a tool that provides an easy way to provide documentation for your code using OpenAI's APIs.  
It comes as a GitHub Action and can be easily integrated into your workflow.  
It can be used, for example, to generate documentation for all files in a folder, specific files, or only files that have been modified in a pull request. 

## Examples

### Example 1: Generate Documentation for specific folders or files

With this configuration, ZeroDocs action will take the folders or files to scan as input from the UI and generate documentation for them.

```yaml
name: Auto Doc Generation

on:
  workflow_dispatch:
    inputs:
      scan-dir:
        type: string
        description: 'The directory to scan for doc generation'

jobs:
  auto_doc_generation:
    runs-on: ubuntu-latest
    steps:
      - name: Generate Docs
        uses: gianfrancodemarco/zero-docs@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          paths: ${{ github.event.inputs.scan-dir }}
          reviewers: gianfrancodemarco
```

### Example 2: Generate Documentation for modified files in a pull request
```yaml
name: Auto Doc Generation

on:
  push:
    branches:
      - main

jobs:
  fetch_files:
    runs-on: ubuntu-latest
    outputs:
      files: ${{ steps.changed-files.outputs.all_changed_files }}
    steps:

      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # OR "2" -> To retrieve the preceding commit.

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v42
        with:
          since_last_remote_commit: true 

      - name: List all changed files
        env:
          ALL_CHANGED_FILES: ${{ steps.changed-files.outputs.all_changed_files }}
        run: |
          for file in ${ALL_CHANGED_FILES}; do
            echo "$file was changed"
          done

  auto_doc_generation_only_modified_files:
    runs-on: ubuntu-latest
    needs: fetch_files
    steps:
      - name: Generate Docs
        uses: gianfrancodemarco/zero-docs@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          paths: ${{ needs.fetch_files.outputs.files }}
          reviewers: gianfrancodemarco
```

## GitHub Actions Inputs

| Name            | Description                               | Required | Default Value |
|-----------------|-------------------------------------------|----------|---------------|
| openai-api-key  | API key for OpenAI                        | true     | -             |
| reviewers       | A comma or newline-separated list of reviewers (GitHub usernames) to request a review from. (via [create-pull-request](https://github.com/peter-evans/create-pull-request))    | false    | -
| paths           | **Space** separated list of directories and/or files to scan | true     | . (root)     |
| code-entities   | Comma separated list of code entities to generate docstrings for | false    | module,class,function |
| prompt          | Prompt to use for generating docstrings   | false    | (in source code)             |

## Roadmap

1. [X] **Customization Options**: Add an option to allow the choice of which elements to document, such as modules, classes, or functions.
2. [ ] **Grateful ending if no files are found**: Add a message to the logs if no files are found to generate documentation for.
3. [ ] **Add unit tests**
4. [ ] **Generation mode**: Allow for different generations mode, for example:
   1. [ ] Local: send only the module/class/function code to OpenAI
   2. [ ] Context-Aware: send the entire module to OpenAI, so it can understand the context of the code.
   3. [ ] Hybrid: send all the docstrings to OpenAI, and the module/class/function code we are documenting.
5. [ ] **Replace Existing Documentation**: Add a parameter to replace existing documentation if present.
6. [ ] **Parallel Generation**: Add an option to generate documentation in parallel for multiple files.
7. [ ] **Allow for different LLMs to be used**
8. [ ] **Selective Regeneration**: Implement a mechanism to regenerate documentation only for components modified within a PR.
9. [ ] **Standalone Package**: Publish ZeroDocs as a Python package
10. [ ] **Cost Estimation**: Add a preview feature to estimate costs before generating documentation.
11. [ ] **Language Support**: Add support for languages other than Python.


Feel free to contribute to our project and help us make documentation hassle-free! 🚀📚
