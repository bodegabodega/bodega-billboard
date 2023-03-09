const response = (statusCode, body) => {
  return body ? { statusCode, body: JSON.stringify(body, null, 2) } : { statusCode };
}

export const badRequest = response(400);
export const good =  body => response(200, body);
export const internalServerError =  response(500);