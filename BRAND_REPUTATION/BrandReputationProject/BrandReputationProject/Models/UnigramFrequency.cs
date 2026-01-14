using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    [Table("UnigramFrequency")]
    public class UnigramFrequency
    {
        [Key]
        public int ID_uni {get; set;}

        public string BrandName { get; set; }

        public string Platform { get; set; }

        public string Unigram { get; set; }

        public int Frequency { get; set; }
    }
}