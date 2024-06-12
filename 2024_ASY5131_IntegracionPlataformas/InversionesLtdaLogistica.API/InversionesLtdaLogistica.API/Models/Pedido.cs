using System.Collections.Generic;

namespace InversionesLtdaLogistica.API.Models
{
    public class Pedido
    {
        public int Id { get; set; }
        public string Cliente { get; set; }
        public List<Item> Items { get; set; }
        public string MetodoPago { get; set; }
        public string FormaEnvio { get; set; }
        public double Total { get; set; }
        public string FechaHora { get; set; }
        public string Estado { get; set; }

    }


    public class Item
    {
        public int Id { get; set; }
        public string Nombre { get; set; }
        public double Precio { get; set; }
        public int Cantidad { get; set; }
    }
}
