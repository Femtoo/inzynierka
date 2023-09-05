using System.ComponentModel.DataAnnotations;

namespace MedImagesClient.Models
{
    public class AddImageVM
    {
        [Required]
        public string GroupName { get; set; } = string.Empty;
        [Required]
        public string Description { get; set; } = string.Empty;
    }
}
