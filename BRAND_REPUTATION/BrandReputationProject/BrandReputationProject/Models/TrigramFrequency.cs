using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    [Table("TrigramFrequency")]
    public class TrigramFrequency
    {
        [Key]
        public int ID_trig { get; set; }

        public string BrandName { get; set; }

        public string Platform { get; set; }

        public string Trigram { get; set; }

        public int Frequency { get; set; }
    }
}