using Microsoft.EntityFrameworkCore;

namespace InversionesLtda.API.Models
{
    public class Clientecontext : DbContext
    {
        public Clientecontext(DbContextOptions<Clientecontext> options) : base(options) { }
        public DbSet<Cliente> Clientes { get; set; }
    }
}
