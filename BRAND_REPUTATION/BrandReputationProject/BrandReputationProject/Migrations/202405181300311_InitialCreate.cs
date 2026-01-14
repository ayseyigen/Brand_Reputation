namespace BrandReputationProject.Migrations
{
    using System;
    using System.Data.Entity.Migrations;
    
    public partial class InitialCreate : DbMigration
    {
        public override void Up()
        {
            CreateTable(
                "dbo.amazonsingledata",
                c => new
                    {
                        ID_amz = c.Int(nullable: false, identity: true),
                        Catalog_Name = c.String(),
                        Brand_Name = c.String(),
                        Product_Name = c.String(),
                        Price = c.Single(nullable: false),
                        Star = c.Single(nullable: false),
                        NOReviews = c.Single(nullable: false),
                        Comment_Title = c.String(),
                        Comment_Date = c.String(),
                        Comment = c.String(),
                        Date_Collected = c.String(),
                        Time_Collected = c.String(),
                        Label = c.String(),
                        Score = c.Single(nullable: false),
                    })
                .PrimaryKey(t => t.ID_amz);
            
            CreateTable(
                "dbo.__MigrationHistory",
                c => new
                    {
                        MigrationId = c.String(nullable: false, maxLength: 150),
                        ContextKey = c.String(nullable: false, maxLength: 300),
                        Model = c.Binary(nullable: false),
                        ProductVersion = c.String(nullable: false, maxLength: 32),
                    })
                .PrimaryKey(t => new { t.MigrationId, t.ContextKey });
            
            CreateTable(
                "dbo.instagramdata",
                c => new
                    {
                        ID_ins = c.Int(nullable: false, identity: true),
                        BrandName = c.String(),
                        Post_Amount = c.Single(nullable: false),
                        Followers = c.Int(nullable: false),
                        Follows = c.Int(nullable: false),
                        Likes = c.Single(nullable: false),
                        Post_Send_Date = c.String(),
                        Post_Description = c.String(),
                        Post_Comment = c.String(),
                        Comment_Date = c.String(),
                        Data_Collected_Date = c.String(),
                        Data_Collected_Time = c.String(),
                        Label = c.String(),
                        Score = c.Single(nullable: false),
                    })
                .PrimaryKey(t => t.ID_ins);
            
            CreateTable(
                "dbo.sikayetsingledata",
                c => new
                    {
                        ID_sikayet = c.Int(nullable: false, identity: true),
                        Brand = c.String(),
                        Date = c.String(),
                        Comment = c.String(),
                        Label = c.String(),
                        Score = c.Single(nullable: false),
                    })
                .PrimaryKey(t => t.ID_sikayet);
            
            CreateTable(
                "dbo.twittersingledata",
                c => new
                    {
                        ID_twi = c.Int(nullable: false, identity: true),
                        Brand = c.String(),
                        Date = c.String(),
                        Comment = c.String(),
                        Label = c.String(),
                        Score = c.Single(nullable: false),
                    })
                .PrimaryKey(t => t.ID_twi);
            
        }
        
        public override void Down()
        {
            DropTable("dbo.twittersingledata");
            DropTable("dbo.sikayetsingledata");
            DropTable("dbo.instagramdata");
            DropTable("dbo.__MigrationHistory");
            DropTable("dbo.amazonsingledata");
        }
    }
}
