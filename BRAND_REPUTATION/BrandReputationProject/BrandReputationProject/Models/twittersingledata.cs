namespace BrandReputationProject.Models
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("twittersingledata")]
    public partial class twittersingledata
    {
        [StringLength(50)]
        public string Brand { get; set; }

        [StringLength(20)]
        public string Date { get; set; }

        public string Comment { get; set; }

        [StringLength(20)]
        public string Label { get; set; }

        public double? Score { get; set; }

        [Key]
        public int ID_twi { get; set; }
    }
}
