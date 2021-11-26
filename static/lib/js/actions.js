class Request {
    constructor(csrfToken) {
      this.csrfToken = csrfToken;
    }
  
    async get(url) {
      const response = await fetch(url);
      const responseData = await response.json();
  
      return responseData;
    }
  
    async get_r(url) {
      const response = await fetch(url);
  
      return response;
    }
  
    async post(url, data) {
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      const responseData = await response.json();
      return responseData;
    }
  
    async post_r(url, data) {
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      return response;
    }
  
    async post_file(url, data) {
      const response = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
          "X-CSRFToken": this.csrfToken
        },
      });
      return response;
    }
  
    async patch(url, data) {
      const response = await fetch(url, {
        method: "PATCH",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      const responseData = await response.json();
      return responseData;
    }
  
    async patch_r(url, data) {
      const response = await fetch(url, {
        method: "PATCH",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      return response;
    }
  
    async put(url, data) {
      const response = await fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      const responseData = await response.json();
      return responseData;
    }
  
    async put_r(url, data) {
      const response = await fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      return response;
    }
  
    async put_file(url, data) {
      const response = await fetch(url, {
        method: "PUT",
        body: data,
        headers: {
          "X-CSRFToken": this.csrfToken,
        },
      });
      return response;
    }
  
    async delete(url) {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      return "Data has been deleted";
    }
  
    async delete_r(url) {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": this.csrfToken,
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      return response;
    }
  }
  