# async-lambda

`async-lambda` is a framework for creating `AWS Lambda` applications with built
in support for asynchronous invocation via a SQS Queue. This is useful if you
have workloads you need to split up into separate execution contexts.

`async-lambda` converts your application into a `Serverless Application Model (SAM)`
template which can be deployed with the `SAM` cli tool.

## Generate SAM template

Utilize the `async-lambda` CLI tool to generate a SAM template and function bundle.

```bash
async-lambda build app
```

## Deploy SAM Template

Deploy the generated `SAM` template with the `SAM` CLI.

```bash
sam deploy --guided
```

# Known Limitations

- The `async_invoke` payload must be `JSON` serializable with `json.dumps`.
- It is possible to get into infinite loops quite easily. (Task A invokes Task B, Task B invokes Task A)
