using System;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.Entity;
using System.Linq;

namespace BrandReputationProject.Models
{
    public partial class BrandContext : DbContext
    {
        public BrandContext()
            : base("name=BrandContext")
        {
        }

        public virtual DbSet<C__MigrationHistory> C__MigrationHistory { get; set; }
        public virtual DbSet<amazonsingledata> amazonsingledata { get; set; }
        public virtual DbSet<instagramdata> instagramsingledata { get; set; }
        public virtual DbSet<twittersingledata> twittersingledata { get; set; }
        public virtual DbSet<UnigramFrequency> unigramfrequency { get; set; }
        public virtual DbSet<TrigramFrequency> trigramfrequency { get; set; }
        public virtual DbSet<BigramFrequency> bigramfrequency { get; set; }
        public virtual DbSet<sikayetsingledata> sikayetsingledata { get; set; }
        public virtual DbSet<BrandSentiments> brandsentiments { get; set; }
        public virtual DbSet<Hashtags> hashtags { get; set; }
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
        }
    }
}
