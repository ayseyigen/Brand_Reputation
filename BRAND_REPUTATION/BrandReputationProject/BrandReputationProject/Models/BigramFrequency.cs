using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Drawing;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    [Table("BigramFrequency")]
    public class BigramFrequency
    {
        [Key]
        public int ID_big {  get; set; }

        public string BrandName { get; set; }

        public string Platform { get; set;}

        public string Bigram { get; set; }

        public int Frequency { get; set; }

    }
}