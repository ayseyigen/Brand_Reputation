namespace BrandReputationProject.Models
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("amazonsingledata")]
    public partial class amazonsingledata
    {
        [StringLength(100)]
        public string Catalog_Name { get; set; }

        [StringLength(200)]
        public string Brand_Name { get; set; }

        [StringLength(500)]
        public string Product_Name { get; set; }

        public double Price { get; set; }

        public double Star { get; set; }

        public double NOReviews { get; set; }

        public string Comment_Title { get; set; }

        [StringLength(20)]
        public string Comment_Date { get; set; }

        public string Comment { get; set; }

        [StringLength(20)]
        public string Date_Collected { get; set; }

        [StringLength(20)]
        public string Time_Collected { get; set; }

        [StringLength(20)]
        public string Label { get; set; }

        public double Score { get; set; }

        [Key]
        public int ID_amz { get; set; }
    }
}
