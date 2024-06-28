using Microsoft.EntityFrameworkCore;
using InversionesLtdaProductos.API.Models;

public class Productocontext : DbContext
{
    public Productocontext (DbContextOptions<Productocontext> options) : base(options) { }

    public DbSet<Producto> Productos { get; set; }
}
