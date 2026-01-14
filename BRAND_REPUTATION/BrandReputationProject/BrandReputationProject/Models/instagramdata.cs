namespace BrandReputationProject.Models
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("instagramdata")]
    public partial class instagramdata
    {
        [StringLength(50)]
        public string BrandName { get; set; }

        public double? Post_Amount { get; set; }

        public int? Followers { get; set; }

        public int? Follows { get; set; }

        public double Likes { get; set; }

        [StringLength(15)]
        public string Post_Send_Date { get; set; }

        public string Post_Description { get; set; }

        public string Post_Comment { get; set; }

        [StringLength(15)]
        public string Comment_Date { get; set; }

        [StringLength(15)]
        public string Data_Collected_Date { get; set; }

        [StringLength(15)]
        public string Data_Collected_Time { get; set; }

        [StringLength(12)]
        public string Label { get; set; }

        public double? Score { get; set; }

        [Key]
        public int ID_ins { get; set; }
    }
}
