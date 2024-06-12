using InversionesLtdaLogistica.API.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Linq;
using System.Collections.Generic;

namespace InversionesLtdaLogistica.API.Controllers
{
        [Route("api/[controller]")]
        [ApiController]
        public class PedidoController : ControllerBase
        {
            private static List<Pedido> pedidos = new List<Pedido>();

            [HttpGet]
            public ActionResult<IEnumerable<Pedido>> Get()
            {
                return pedidos;
            }

            [HttpGet("{id}")]
            public ActionResult<Pedido> Get(int id)
            {
                var pedido = pedidos.FirstOrDefault(p => p.Id == id);
                if (pedido == null)
                {
                    return NotFound();
                }
                return pedido;
            }

            [HttpPost]
            public ActionResult<Pedido> Post([FromBody] Pedido pedido)
            {
                pedido.Id = pedidos.Count > 0 ? pedidos.Max(p => p.Id) + 1 : 1;
                pedido.Estado = "Pendiente";
                pedidos.Add(pedido);
                return CreatedAtAction(nameof(Get), new { id = pedido.Id }, pedido);
            }

            [HttpPut("{id}")]
            public ActionResult<Pedido> Put(int id, [FromBody] Pedido updatedPedido)
            {
                var pedido = pedidos.FirstOrDefault(p => p.Id == id);
                if (pedido == null)
                {
                    return NotFound();
                }

                pedido.Estado = updatedPedido.Estado;
                return pedido;
            }

            [HttpDelete("{id}")]
            public IActionResult Delete(int id)
            {
                var pedido = pedidos.FirstOrDefault(p => p.Id == id);
                if (pedido == null)
                {
                    return NotFound();
                }

                pedidos.Remove(pedido);
                return NoContent();
            }
        }
    }
