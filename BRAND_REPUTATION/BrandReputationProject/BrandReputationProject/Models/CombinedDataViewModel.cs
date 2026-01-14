using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace BrandReputationProject.Models
{
    public class CombinedDataViewModel
    {
        public List<amazonsingledata> AmazonSingleData { get; set; }

        public List<instagramdata> InstagramSingleData { get; set; }

        public List<sikayetsingledata> SikayetSingleData { get;set; }

        public List<twittersingledata> Twittersingledatas { get; set; }

        public List<UnigramFrequency> UnigramFrequencies { get; set; }

        public List<BigramFrequency> BigramFrequencies { get; set;}

        public List<TrigramFrequency> TrigramFrequencies { get;set; }

        public List<BrandSentiments> BrandSentiments { get;  set; }
        public List<Hashtags> Hashtags { get; set; }
    }
}