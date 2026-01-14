using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    [Table("BrandSentiments")]
    public class BrandSentiments
    {
        [Key]
        public int ID_sent { get; set; }

        public string BrandName { get; set; }

        public string Platform { get; set; }

        public int Positive { get; set; }

        public int Negative { get; set; }

        public int Neutral { get; set; }

        public int Total { get; set; }

        public string WordCloud { get; set; }
    }
}