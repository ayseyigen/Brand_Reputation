using BrandReputationProject.Models;
using System;
using System.Collections.Generic;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.UI.WebControls;

namespace BrandReputationProject.Controllers
{
    public class HomeController : Controller
    {
        private BrandContext db = new BrandContext();
        public ActionResult Index(string term)
        {
            if (!string.IsNullOrEmpty(term))
            {

                var catalog = db.amazonsingledata.FirstOrDefault(p => p.Catalog_Name.ToLower().Contains(term.ToLower()));
                if (catalog != null)
                {
                    
                    return RedirectToAction("Brand", "Home", new { catalogname = catalog.Catalog_Name });
                }
                else
                {
                    
                    var brand = db.amazonsingledata.FirstOrDefault(b => b.Brand_Name.ToLower().Contains(term.ToLower()));

                    var tBrand= db.twittersingledata.FirstOrDefault(b => b.Brand.ToLower().Contains(term.ToLower()));

                    var sBrand= db.sikayetsingledata.FirstOrDefault(b => b.Brand.ToLower().Contains(term.ToLower()));

                    var iBrand = db.instagramsingledata.FirstOrDefault(b => b.BrandName.ToLower().Contains(term.ToLower()));

                    if (brand != null) 
                    {
                        
                        return RedirectToAction("Detail", "Home", new { brandname = brand.Brand_Name });
                    }
                    else if(tBrand!=null)
                    {
                        return RedirectToAction("Detail", "Home", new { brandname = tBrand.Brand });
                    }
                    else if (sBrand != null)
                    {
                        return RedirectToAction("Detail", "Home", new { brandname = sBrand.Brand });
                    }
                    else if (iBrand != null)
                    {
                        return RedirectToAction("Detail", "Home", new { brandname = iBrand.BrandName });
                    }
                    else
                    {
                        ViewBag.Message = "No data found for the search term: " + term;
                    }
                }
            }
            var viewModel = db.amazonsingledata.ToList();
            return View(viewModel);
        }


        public ActionResult Brand(string catalogname)
        {
            if (!string.IsNullOrEmpty(catalogname))
            {
                var viewModel = db.amazonsingledata
                                   .Where(p => p.Catalog_Name.ToLower() == catalogname.ToLower())
                                   .Select(b => b.Brand_Name)
                                   .Distinct()
                                   .ToList();

                if (viewModel.Count == 0)
                {
                    ViewBag.Message = "No data found for the search term: " + catalogname;
                }
                return View(viewModel);
            }

            return RedirectToAction("Index");
        }


        public ActionResult Detail(string brandname)
        {
            CombinedDataViewModel viewModel = new CombinedDataViewModel();
            int isBrandInTwitterData = 0;
            int isBrandInSikayetData = 0;
            int isBrandInAmazonData = 0;
            int isBrandInInstagramData = 0;

            int isBrandInHashtags = 0;

            int isTwitterSentiments = 0;
            int isSikayetSentiments = 0;
            int isInstagramSentiments = 0;
            int isAmazonSentiments = 0;

            int isTwitterUni = 0;
            int isSikayetUni = 0;
            int isInstagramUni = 0;
            int isAmazonUni = 0;

            int isTwitterTri = 0;
            int isSikayetTri = 0;
            int isInstagramTri = 0;
            int isAmazonTri = 0;

            int isTwitterBig = 0;
            int isSikayetBig = 0;
            int isInstagramBig = 0;
            int isAmazonBig = 0;

            if (!string.IsNullOrEmpty(brandname))
            {
                if (db.sikayetsingledata.Any(s => s.Brand.ToLower() == brandname.ToLower()))
                {
                    isBrandInSikayetData = 1;
                    viewModel.SikayetSingleData = db.sikayetsingledata.Where(s => s.Brand.ToLower() == brandname.ToLower()).ToList();
                }

                if (db.amazonsingledata.Any(p => p.Brand_Name.ToLower() == brandname.ToLower()))
                {
                    isBrandInAmazonData = 1;
                    viewModel.AmazonSingleData = db.amazonsingledata.Where(p => p.Brand_Name.ToLower() == brandname.ToLower()).ToList();
                }

                if (db.instagramsingledata.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {
                    isBrandInInstagramData = 1;
                    viewModel.InstagramSingleData = db.instagramsingledata.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                }

                if (db.twittersingledata.Any(p => p.Brand.ToLower() == brandname.ToLower()))
                {
                    viewModel.Twittersingledatas = db.twittersingledata.Where(p => p.Brand.ToLower() == brandname.ToLower()).ToList();
                    isBrandInTwitterData = 1;
                }

                if (db.hashtags.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {
                    viewModel.Hashtags = db.hashtags.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                    isBrandInHashtags = 1;
                }
                //BrandSentiment
                if (db.brandsentiments.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {

                    if (db.brandsentiments.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Twitter"))
                    {
                        viewModel.BrandSentiments = db.brandsentiments.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isTwitterSentiments = 1;
                    }

                    if (db.brandsentiments.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Şikayet Var"))
                    {
                        viewModel.BrandSentiments = db.brandsentiments.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isSikayetSentiments = 1;
                    }
                    if (db.brandsentiments.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Instagram"))
                    {
                        viewModel.BrandSentiments = db.brandsentiments.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isInstagramSentiments = 1;
                    }
                    if (db.brandsentiments.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Amazon"))
                    {
                        viewModel.BrandSentiments = db.brandsentiments.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isAmazonSentiments = 1;
                    }

                }
                //UnigramFrequency
                if (db.unigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {

                    if (db.unigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Twitter"))
                    {
                        viewModel.UnigramFrequencies = db.unigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isTwitterUni = 1;
                    }

                    if (db.unigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Şikayet Var"))
                    {
                        viewModel.UnigramFrequencies = db.unigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isSikayetUni = 1;
                    }
                    if (db.unigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Instagram"))
                    {
                        viewModel.UnigramFrequencies = db.unigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isInstagramUni = 1;
                    }
                    if (db.unigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Amazon"))
                    {
                        viewModel.UnigramFrequencies = db.unigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isAmazonUni = 1;
                    }

                }
                //TrigramFrequency
                if (db.trigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {

                    if (db.trigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Twitter"))
                    {
                        viewModel.TrigramFrequencies = db.trigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isTwitterTri = 1;
                    }

                    if (db.trigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Şikayet Var"))
                    {
                        viewModel.TrigramFrequencies = db.trigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isSikayetTri = 1;
                    }
                    if (db.trigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Instagram"))
                    {
                        viewModel.TrigramFrequencies = db.trigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isInstagramTri = 1;
                    }
                    if (db.trigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Amazon"))
                    {
                        viewModel.TrigramFrequencies = db.trigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isAmazonTri = 1;
                    }

                }
                //BigramFrequeny
                if (db.bigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower()))
                {

                    if (db.bigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Twitter"))
                    {
                        viewModel.BigramFrequencies = db.bigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isTwitterBig = 1;
                    }

                    if (db.bigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Şikayet Var"))
                    {
                        viewModel.BigramFrequencies = db.bigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isSikayetBig = 1;
                    }
                    if (db.bigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Instagram"))
                    {
                        viewModel.BigramFrequencies = db.bigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isInstagramBig = 1;
                    }
                    if (db.bigramfrequency.Any(p => p.BrandName.ToLower() == brandname.ToLower() && p.Platform == "Amazon"))
                    {
                        viewModel.BigramFrequencies = db.bigramfrequency.Where(p => p.BrandName.ToLower() == brandname.ToLower()).ToList();
                        isAmazonBig = 1;
                    }

                }



                ViewBag.BrandName = brandname;

                ViewBag.Sentiment_S = isSikayetSentiments;
                ViewBag.Sentiment_I= isInstagramSentiments;
                ViewBag.Sentiment_A= isAmazonSentiments;
                ViewBag.Sentiment_T = isTwitterSentiments;

                ViewBag.Uni_S = isSikayetUni;
                ViewBag.Uni_I = isInstagramUni;
                ViewBag.Uni_A = isAmazonUni;
                ViewBag.Uni_T = isTwitterUni;

                ViewBag.Tri_S = isSikayetTri;
                ViewBag.Tri_I = isInstagramTri;
                ViewBag.Tri_A = isAmazonTri;
                ViewBag.Tri_T = isTwitterTri;

                ViewBag.Big_S = isSikayetBig;
                ViewBag.Big_I = isInstagramBig;
                ViewBag.Big_A = isAmazonBig;
                ViewBag.Big_T = isTwitterBig;

                ViewBag.Hashtags = isBrandInHashtags;

                ViewBag.Sikayet = isBrandInSikayetData;
                ViewBag.Amazon = isBrandInAmazonData;
                ViewBag.Instagram = isBrandInInstagramData;
                ViewBag.Twitter = isBrandInTwitterData;

                //Count positive, negative, and neutral comments for each data set
                ViewBag.PositiveCount_S = viewModel.SikayetSingleData?.Count(t => t.Label == "positive") ?? 0;
                ViewBag.NegativeCount_S = viewModel.SikayetSingleData?.Count(t => t.Label == "negative") ?? 0;
                ViewBag.NeutralCount_S = viewModel.SikayetSingleData?.Count(t => t.Label == "neutral") ?? 0;

                ViewBag.PositiveCount_A = viewModel.AmazonSingleData?.Count(t => t.Label == "positive") ?? 0;
                ViewBag.NegativeCount_A = viewModel.AmazonSingleData?.Count(t => t.Label == "negative") ?? 0;
                ViewBag.NeutralCount_A = viewModel.AmazonSingleData?.Count(t => t.Label == "neutral") ?? 0;

                ViewBag.PositiveCount_I = viewModel.InstagramSingleData?.Count(t => t.Label == "positive") ?? 0;
                ViewBag.NegativeCount_I = viewModel.InstagramSingleData?.Count(t => t.Label == "negative") ?? 0;
                ViewBag.NeutralCount_I = viewModel.InstagramSingleData?.Count(t => t.Label == "neutral") ?? 0;

                ViewBag.PositiveCount_T = viewModel.Twittersingledatas?.Count(t => t.Label == "positive") ?? 0;
                ViewBag.NegativeCount_T = viewModel.Twittersingledatas?.Count(t => t.Label == "negative") ?? 0;
                ViewBag.NeutralCount_T = viewModel.Twittersingledatas?.Count(t => t.Label == "neutral") ?? 0;

                return View(viewModel);
            }

            ViewBag.Message = "No brand name provided.";
            return RedirectToAction("Index");
        }




        public ActionResult DetailS(string productname)
        {
            if (!string.IsNullOrEmpty(productname))
            {
                var viewModel = db.amazonsingledata
                                   .Where(p => p.Product_Name.ToLower() == productname.ToLower())
                                   .Distinct()
                                   .ToList();
                if (productname == null)
                {
                    ViewBag.Message = "No data found for the search term: " + productname;
                }
                return View(viewModel);
            }

            return RedirectToAction("Index");
        }

    }
}