namespace BrandReputationProject.Models
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("sikayetsingledata")]
    public partial class sikayetsingledata
    {
        [StringLength(50)]
        public string Brand { get; set; }

        [StringLength(50)]
        public string Date { get; set; }

        public string Comment { get; set; }

        [StringLength(15)]
        public string Label { get; set; }

        public double? Score { get; set; }

        [Key]
        public int ID_sikayet { get; set; }
    }
}
