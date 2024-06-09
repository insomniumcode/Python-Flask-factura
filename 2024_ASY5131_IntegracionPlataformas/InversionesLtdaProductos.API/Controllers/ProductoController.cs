using System.Collections.Generic;
using System;
using InversionesLtdaProductos.API.Models;
using Microsoft.AspNetCore.Mvc;
using System.Linq;

namespace InversionesLtdaProductos.API.Controllers
{

    [Route("api/Producto")]
    [ApiController]

    public class ProductoController : ControllerBase
    {
        private static IList<Producto> lista = new List<Producto>();

        // GET: api/<ClienteController>
        [HttpGet]
        public IEnumerable<Producto> Get()
        {
            return lista;
        }

        // GET 
        [HttpGet("{id}")]
        public Producto Get(int id)
        {
            return lista.FirstOrDefault(x => x.id == id);
        }

        // POST 
        [HttpPost]
        public void Post([FromBody] Producto value)
        {
            lista.Add(value);
        }

        // PUT 
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] Producto value)
        {
            Producto selection = lista.FirstOrDefault(x => x.id == id);
            lista[lista.IndexOf(selection)] = value;
        }

        // DELETE 
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
            lista.Remove(lista.FirstOrDefault(x => x.id == id));
        }

        // PUT: descuento de stock
        [HttpPut("{id}/DescuentoStock")]
        public IActionResult DescuentoStock(int id, [FromBody] int cantidad)
        {
            var producto = lista.FirstOrDefault(x => x.id == id);
            if (producto == null)
            {
                return NotFound();
            }
            if (producto.Stock < cantidad)
            {
                return BadRequest("Stock insuficiente.");
            }
            producto.Stock -= cantidad;
            return NoContent();
        }
    }




}

