using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;
using InversionesLtda.API.Models;

namespace InversionesLtdaClientes.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ClienteController : ControllerBase
    {
        private readonly Clientecontext _context;

        public ClienteController(Clientecontext context)
        {
            _context = context;
        }

        [HttpGet]
        public IEnumerable<Cliente> Get()
        {
            return _context.Clientes.ToList();
        }

        [HttpGet("{id}")]
        public Cliente Get(int id)
        {
            return _context.Clientes.Find(id);
        }

        [HttpPost]
        public void Post([FromBody] Cliente value)
        {
            _context.Clientes.Add(value);
            _context.SaveChanges();
        }

        [HttpPut("{id}")]
        public void Put(int id, [FromBody] Cliente value)
        {
            var cliente = _context.Clientes.Find(id);
            if (cliente != null)

            {
                cliente.id = value.id;
                cliente.razonSocial = value.razonSocial;
                cliente.rut = value.rut;
                cliente.direccion = value.direccion;
                _context.SaveChanges();
            }
        }

        [HttpDelete("{id}")]
        public void Delete(int id)
        {
            var cliente = _context.Clientes.Find(id);
            if (cliente != null)
            {
                _context.Clientes.Remove(cliente);
                _context.SaveChanges();
            }
        }
    }
}