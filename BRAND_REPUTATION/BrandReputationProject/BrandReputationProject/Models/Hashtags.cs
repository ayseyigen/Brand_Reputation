using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    [Table("Hashtags")]
    public class Hashtags
    {
        [Key]
        public int ID_hash { get; set; }

        public string BrandName { get; set; }

        public string Platform { get; set; }

        public string hashtags { get; set; }

        public int Frequency { get; set; }
    }
}