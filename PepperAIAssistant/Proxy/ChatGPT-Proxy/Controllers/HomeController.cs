using Microsoft.AspNetCore.DataProtection.KeyManagement;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Net.Http.Headers;
using Newtonsoft.Json;
using System.Diagnostics;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json.Serialization;

namespace ChatGPT_Proxy.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        [Route("v1/chat/completions")]
        [HttpPost]
        public IActionResult Index()
        {
            HttpClient httpClient = new()
            {
                BaseAddress = new Uri($"https://api.openai.com/"),
            };
            httpClient.DefaultRequestHeaders.Add("Authorization", Request.Headers.Authorization.ToString());
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            using (StreamReader reader = new(Request.Body, Encoding.UTF8))
            {
                string requestBody = reader.ReadToEndAsync().Result;
                var content = new StringContent(requestBody, Encoding.UTF8, "application/json");
                HttpResponseMessage result = httpClient.PostAsync("v1/chat/completions", content).Result;
                if(result.IsSuccessStatusCode)
                {
                    return Content(result.Content.ReadAsStringAsync().Result);
                }
            }
            return NotFound();
        }
    }
}
